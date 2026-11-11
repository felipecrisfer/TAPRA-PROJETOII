import logging
import os

import azure.functions as func
import pyodbc

app = func.FunctionApp()

SCHEMA = "itsm"
BATCH_SIZE = 1000

TABELAS = [
    "analista",
    "categoria",
    "cliente_organizacao",
    "fila",
    "sla",
    "solicitante",
    "chamado",
    "chamado_sla",
    "chamado_status_historico",
    "csat_avaliacao",
]

def montar_conn_str(host, database, user, password):
    return (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={host};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )


def conectar_origem():
    return pyodbc.connect(
        montar_conn_str(
            os.environ["HOST"],
            os.environ["DATABASE"],
            os.environ["USER"],
            os.environ["PASSWORD"],
        )
    )


def conectar_destino():
    return pyodbc.connect(
        montar_conn_str(
            os.environ["DEST_HOST"],
            os.environ["DEST_DATABASE"],
            os.environ["DEST_USER"],
            os.environ["DEST_PASSWORD"],
        )
    )

def copiar_tabela(src, dst, tabela):
    dst_cur = dst.cursor()

    colunas_destino = {
        r.column_name for r in dst_cur.columns(table=tabela, schema=SCHEMA)
    }
    if not colunas_destino:
        raise ValueError(f"Tabela {SCHEMA}.{tabela} não existe no destino")

    pks = [r.column_name for r in dst_cur.primaryKeys(table=tabela, schema=SCHEMA)]
    if not pks:
        raise ValueError(f"{SCHEMA}.{tabela} não tem chave primária no destino")


    src_cur = src.cursor()
    src_cur.execute(f"SELECT * FROM {SCHEMA}.{tabela}")

    todas_origem = [c[0] for c in src_cur.description]
    colunas = [c for c in todas_origem if c in colunas_destino]
    idx = [todas_origem.index(c) for c in colunas]

    cols = ", ".join(f"[{c}]" for c in colunas)
    params = ", ".join("?" for _ in colunas)
    on = " AND ".join(f"t.[{k}] = s.[{k}]" for k in pks)
    sets = ", ".join(f"t.[{c}] = s.[{c}]" for c in colunas if c not in pks)
    valores = ", ".join(f"s.[{c}]" for c in colunas)

    merge = (
        f"MERGE {SCHEMA}.{tabela} AS t "
        f"USING (VALUES ({params})) AS s ({cols}) ON {on} "
    )
    if sets:
        merge += f"WHEN MATCHED THEN UPDATE SET {sets} "
    merge += f"WHEN NOT MATCHED THEN INSERT ({cols}) VALUES ({valores});"

    
    tem_identity = (
        dst_cur.execute(
            "SELECT OBJECTPROPERTY(OBJECT_ID(?), 'TableHasIdentity')",
            f"{SCHEMA}.{tabela}",
        ).fetchone()[0]
        == 1
    )

    if tem_identity:
        dst_cur.execute(f"SET IDENTITY_INSERT {SCHEMA}.{tabela} ON")

    total = 0
    try:
        while True:
            lote = src_cur.fetchmany(BATCH_SIZE)
            if not lote:
                break
            dados = [tuple(linha[i] for i in idx) for linha in lote]
            dst_cur.executemany(merge, dados)
            total += len(dados)
    finally:
        if tem_identity:
            dst_cur.execute(f"SET IDENTITY_INSERT {SCHEMA}.{tabela} OFF")

    logging.info(f"{SCHEMA}.{tabela}: {total} linhas processadas")


@app.timer_trigger(
    schedule="0 0 3 * * *",
    arg_name="myTimer",
    run_on_startup=False, 
    use_monitor=False,
)
def popular_tabelas(myTimer: func.TimerRequest) -> None:
    logging.info("Iniciando carga diária")

    src = conectar_origem()
    dst = conectar_destino()
    try:
        for tabela in TABELAS:
            try:
                copiar_tabela(src, dst, tabela)
                dst.commit()
            except Exception as e:
                dst.rollback()
                logging.error(f"Erro ao popular {SCHEMA}.{tabela}: {e}")
                raise  
    finally:
        src.close()
        dst.close()

    logging.info("Carga diária finalizada")
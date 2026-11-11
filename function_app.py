import logging
import os

import azure.functions as func
import pyodbc

app = func.FunctionApp()

SCHEMA = "itsm"
BATCH_SIZE = 1000


TABELAS = [
    "categoria",
    "cliente_organizacao",
    "fila",
    "sla",
    "analista",
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


def coluna_chave(dst_cur, tabela, colunas_destino):
    row = dst_cur.execute(
        "SELECT name FROM sys.identity_columns WHERE object_id = OBJECT_ID(?)",
        f"{SCHEMA}.{tabela}",
    ).fetchone()
    return row[0] if row else colunas_destino[0]  


def copiar_tabela(src, dst, tabela):
    dst_cur = dst.cursor()

    colunas_destino = [
        r.column_name for r in dst_cur.columns(table=tabela, schema=SCHEMA)
    ]
    if not colunas_destino:
        raise ValueError(f"Tabela {SCHEMA}.{tabela} não existe no destino")

    chave = coluna_chave(dst_cur, tabela, colunas_destino)

    src_cur = src.cursor()
    src_cur.execute(f"SELECT * FROM {SCHEMA}.{tabela}")


    todas_origem = [c[0] for c in src_cur.description]
    colunas = [c for c in todas_origem if c in colunas_destino]
    if chave not in colunas:
        raise ValueError(f"{SCHEMA}.{tabela}: coluna chave '{chave}' não vem da origem")
    idx = [todas_origem.index(c) for c in colunas]
    pos_chave = colunas.index(chave)


    existentes = {
        r[0] for r in dst.cursor().execute(f"SELECT [{chave}] FROM {SCHEMA}.{tabela}")
    }

    cols = ", ".join(f"[{c}]" for c in colunas)
    params = ", ".join("?" for _ in colunas)
    insert = f"INSERT INTO {SCHEMA}.{tabela} ({cols}) VALUES ({params})"

    tem_identity = (
        dst_cur.execute(
            "SELECT OBJECTPROPERTY(OBJECT_ID(?), 'TableHasIdentity')",
            f"{SCHEMA}.{tabela}",
        ).fetchone()[0]
        == 1
    )
    if tem_identity:
        dst_cur.execute(f"SET IDENTITY_INSERT {SCHEMA}.{tabela} ON")

    inseridas = 0
    ignoradas = 0
    try:
        while True:
            lote = src_cur.fetchmany(BATCH_SIZE)
            if not lote:
                break
            dados = []
            for linha in lote:
                valores = tuple(linha[i] for i in idx)
                if valores[pos_chave] in existentes:
                    ignoradas += 1
                    continue
                existentes.add(valores[pos_chave])
                dados.append(valores)
            if dados:
                dst_cur.executemany(insert, dados)
                inseridas += len(dados)
    finally:
        if tem_identity:
            dst_cur.execute(f"SET IDENTITY_INSERT {SCHEMA}.{tabela} OFF")

    logging.info(
        f"{SCHEMA}.{tabela}: {inseridas} linhas novas inseridas, "
        f"{ignoradas} já existiam"
    )

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
            copiar_tabela(src, dst, tabela)
        dst.commit()  
    except Exception as e:
        dst.rollback()
        logging.error(f"Erro na carga, nenhuma alteração foi gravada: {e}")
        raise
    finally:
        src.close()
        dst.close()

    logging.info("Carga diária finalizada")
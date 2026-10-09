import logging
import azure.functions as func
import os
import pyodbc

app = func.FunctionApp()


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_analista(myTimer: func.TimerRequest) -> None:
    logging.info('tabela analista')

    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}')

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            query = "select * from itsm.analista"

            cursor.execute(query)
            rows = cursor.fetchall()

            logging.info(rows)

    except Exception as e:
        logging.error(f"Erro ao ler itsm.analista: {str(e)}")
        raise


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_categoria(myTimer: func.TimerRequest) -> None:
    logging.info('tabela categoria')

    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}')

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            query = "select * from itsm.categoria"

            cursor.execute(query)
            rows = cursor.fetchall()

            logging.info(rows)

    except Exception as e:
        logging.error(f"Erro ao ler itsm.categoria: {str(e)}")
        raise


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_chamado(myTimer: func.TimerRequest) -> None:
    logging.info('tabela chamado')

    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}')

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            query = "select * from itsm.chamado"

            cursor.execute(query)
            rows = cursor.fetchall()

            logging.info(rows)

    except Exception as e:
        logging.error(f"Erro ao ler itsm.chamado: {str(e)}")
        raise


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_chamado_sla(myTimer: func.TimerRequest) -> None:
    logging.info('tabela chamado_sla')

    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}')

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            query = "select * from itsm.chamado_sla"

            cursor.execute(query)
            rows = cursor.fetchall()

            logging.info(rows)

    except Exception as e:
        logging.error(f"Erro ao ler itsm.chamado_sla: {str(e)}")
        raise


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_chamado_status_historico(myTimer: func.TimerRequest) -> None:
    logging.info('tabela chamado_status_historico')

    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}')

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            query = "select * from itsm.chamado_status_historico"

            cursor.execute(query)
            rows = cursor.fetchall()

            logging.info(rows)

    except Exception as e:
        logging.error(f"Erro ao ler itsm.chamado_status_historico: {str(e)}")
        raise

    @app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_cliente_organizacao(myTimer: func.TimerRequest) -> None:
    logging.info('tabela cliente_organizacao')

    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}')

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            query = "select * from itsm.cliente_organizacao"

            cursor.execute(query)
            rows = cursor.fetchall()

            logging.info(rows)

    except Exception as e:
        logging.error(f"Erro ao ler itsm.cliente_organizacao: {str(e)}")
        raise


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_csat_avaliacao(myTimer: func.TimerRequest) -> None:
    logging.info('tabela csat_avaliacao')

    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}')

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            query = "select * from itsm.csat_avaliacao"

            cursor.execute(query)
            rows = cursor.fetchall()

            logging.info(rows)

    except Exception as e:
        logging.error(f"Erro ao ler itsm.csat_avaliacao: {str(e)}")
        raise


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_fila(myTimer: func.TimerRequest) -> None:
    logging.info('tabela fila')

    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}')

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            query = "select * from itsm.fila"

            cursor.execute(query)
            rows = cursor.fetchall()

            logging.info(rows)

    except Exception as e:
        logging.error(f"Erro ao ler itsm.fila: {str(e)}")
        raise


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_sla(myTimer: func.TimerRequest) -> None:
    logging.info('tabela sla')

    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}')

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            query = "select * from itsm.sla"

            cursor.execute(query)
            rows = cursor.fetchall()

            logging.info(rows)

    except Exception as e:
        logging.error(f"Erro ao ler itsm.sla: {str(e)}")
        raise


@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def extract_solicitante(myTimer: func.TimerRequest) -> None:
    logging.info('tabela solicitante')

    sql_server = os.getenv("HOST")
    sql_database = os.getenv("DATABASE")
    sql_user = os.getenv("USER")
    sql_pass = os.getenv("PASSWORD")

    logging.info(f'servidor={sql_server}, banco de dados={sql_database}, usuario={sql_user}')

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            query = "select * from itsm.solicitante"

            cursor.execute(query)
            rows = cursor.fetchall()

            logging.info(rows)

    except Exception as e:
        logging.error(f"Erro ao ler itsm.solicitante: {str(e)}")
        raise
import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).parent / "amei_nota_zero.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def consultar_uploads():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM uploads")
    uploads = cursor.fetchall()

    print("\n===== UPLOADS =====")

    for upload in uploads:
        print(upload)

    conexao.close()


def consultar_logs():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM logs_sistema")
    logs = cursor.fetchall()

    print("\n===== LOGS DO SISTEMA =====")

    for log in logs:
        print(log)

    conexao.close()


def consultar_erros():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM erros_sistema")
    erros = cursor.fetchall()

    print("\n===== ERROS DO SISTEMA =====")

    for erro in erros:
        print(erro)

    conexao.close()


def consultar_performance():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM metricas_performance")
    metricas = cursor.fetchall()

    print("\n===== MÉTRICAS DE PERFORMANCE =====")

    for metrica in metricas:
        print(metrica)

    conexao.close()


consultar_uploads()
consultar_logs()
consultar_erros()
consultar_performance()
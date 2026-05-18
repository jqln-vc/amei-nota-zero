import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).parent / "amei_nota_zero.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def total_uploads():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM uploads")
    total = cursor.fetchone()[0]

    conexao.close()

    print(f"Total de uploads registrados: {total}")


def uploads_por_tipo():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            tipo_arquivo,
            COUNT(*) AS total
        FROM uploads
        GROUP BY tipo_arquivo
    """)

    resultados = cursor.fetchall()
    conexao.close()

    print("\nUploads por tipo de arquivo:")

    for tipo, total in resultados:
        print(f"- {tipo}: {total}")


def tempo_medio_por_funcionalidade():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            funcionalidade,
            ROUND(AVG(tempo_resposta_ms), 2) AS tempo_medio_ms,
            COUNT(*) AS total_execucoes
        FROM metricas_performance
        GROUP BY funcionalidade
    """)

    resultados = cursor.fetchall()
    conexao.close()

    print("\nTempo médio por funcionalidade:")

    for funcionalidade, tempo_medio, total in resultados:
        print(f"- {funcionalidade}: {tempo_medio} ms em {total} execução(ões)")


def erros_por_modulo():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            modulo,
            COUNT(*) AS total_erros
        FROM erros_sistema
        GROUP BY modulo
    """)

    resultados = cursor.fetchall()
    conexao.close()

    print("\nErros por módulo:")

    if len(resultados) == 0:
        print("- Nenhum erro registrado.")
    else:
        for modulo, total in resultados:
            print(f"- {modulo}: {total} erro(s)")


def logs_por_modulo():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            modulo,
            COUNT(*) AS total_logs
        FROM logs_sistema
        GROUP BY modulo
    """)

    resultados = cursor.fetchall()
    conexao.close()

    print("\nLogs por módulo:")

    for modulo, total in resultados:
        print(f"- {modulo}: {total} log(s)")


print("===== RELATÓRIO DE MONITORAMENTO DO SISTEMA =====\n")

total_uploads()
uploads_por_tipo()
tempo_medio_por_funcionalidade()
erros_por_modulo()
logs_por_modulo()
import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).parent / "amei_nota_zero.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


conexao = conectar()
cursor = conexao.cursor()

cursor.execute("DELETE FROM logs_sistema WHERE modulo LIKE '%TESTE%'")
cursor.execute("DELETE FROM erros_sistema WHERE modulo LIKE '%TESTE%'")
cursor.execute("DELETE FROM metricas_performance WHERE funcionalidade LIKE '%Teste%'")

conexao.commit()

print("Linhas removidas do logs_sistema:", cursor.execute("SELECT COUNT(*) FROM logs_sistema WHERE modulo LIKE '%TESTE%'").fetchone()[0])
print("Linhas removidas do erros_sistema:", cursor.execute("SELECT COUNT(*) FROM erros_sistema WHERE modulo LIKE '%TESTE%'").fetchone()[0])
print("Linhas removidas do metricas_performance:", cursor.execute("SELECT COUNT(*) FROM metricas_performance WHERE funcionalidade LIKE '%Teste%'").fetchone()[0])

conexao.close()

print("Limpeza finalizada!")
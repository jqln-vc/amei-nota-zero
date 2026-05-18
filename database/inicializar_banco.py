import sqlite3
from pathlib import Path

CAMINHO_PASTA = Path(__file__).parent
CAMINHO_BANCO = CAMINHO_PASTA / "amei_nota_zero.db"
CAMINHO_SCHEMA = CAMINHO_PASTA / "schema.sql"


def inicializar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    with open(CAMINHO_SCHEMA, "r", encoding="utf-8") as arquivo:
        script_sql = arquivo.read()

    conexao.executescript(script_sql)
    conexao.commit()
    conexao.close()

    print("Banco de dados criado com sucesso!")


if __name__ == "__main__":
    inicializar_banco()
import sqlite3
import time
from pathlib import Path

CAMINHO_BANCO = Path(__file__).parent / "amei_nota_zero.db"


def conectar():
    return sqlite3.connect(CAMINHO_BANCO)


def registrar_log(nivel, modulo, mensagem):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO logs_sistema (nivel, modulo, mensagem)
        VALUES (?, ?, ?)
        """,
        (nivel, modulo, mensagem)
    )

    conexao.commit()
    conexao.close()


def registrar_erro(modulo, tipo_erro, mensagem_erro):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO erros_sistema (modulo, tipo_erro, mensagem_erro)
        VALUES (?, ?, ?)
        """,
        (modulo, tipo_erro, mensagem_erro)
    )

    conexao.commit()
    conexao.close()


def registrar_performance(funcionalidade, tempo_resposta_ms, status_execucao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO metricas_performance 
        (funcionalidade, tempo_resposta_ms, status_execucao)
        VALUES (?, ?, ?)
        """,
        (funcionalidade, tempo_resposta_ms, status_execucao)
    )

    conexao.commit()
    conexao.close()


def medir_tempo(funcionalidade):
    def decorator(funcao):
        def wrapper(*args, **kwargs):
            inicio = time.time()

            try:
                resultado = funcao(*args, **kwargs)

                fim = time.time()
                tempo_ms = (fim - inicio) * 1000

                registrar_performance(
                    funcionalidade=funcionalidade,
                    tempo_resposta_ms=tempo_ms,
                    status_execucao="SUCESSO"
                )

                return resultado

            except Exception as erro:
                fim = time.time()
                tempo_ms = (fim - inicio) * 1000

                registrar_performance(
                    funcionalidade=funcionalidade,
                    tempo_resposta_ms=tempo_ms,
                    status_execucao="ERRO"
                )

                registrar_erro(
                    modulo=funcionalidade,
                    tipo_erro=type(erro).__name__,
                    mensagem_erro=str(erro)
                )

                raise erro

        return wrapper

    return decorator
def registrar_upload(nome_arquivo, tipo_arquivo, tamanho_kb):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO uploads 
        (nome_arquivo, tipo_arquivo, tamanho_kb)
        VALUES (?, ?, ?)
        """,
        (nome_arquivo, tipo_arquivo, tamanho_kb)
    )

    conexao.commit()

    upload_id = cursor.lastrowid

    conexao.close()

    return upload_id
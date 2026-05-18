import sys
import time
from pathlib import Path

import streamlit as st
import pandas as pd

PASTA_RAIZ = Path(__file__).resolve().parents[1]
sys.path.append(str(PASTA_RAIZ))

from database.monitoramento import registrar_log, registrar_erro, registrar_performance, registrar_upload


def carregar_arquivo():
    arquivo = st.file_uploader(
        "Arraste ou selecione seu arquivo de avaliações",
        type=["csv", "xlsx", "txt", "json"]
    )

    if arquivo is not None:
        inicio = time.time()

        try:
            registrar_log(
                "INFO",
                "UPLOAD",
                f"Arquivo recebido: {arquivo.name}"
            )

            tamanho_kb = len(arquivo.getvalue()) / 1024
            tipo_arquivo = arquivo.name.split(".")[-1]

            registrar_upload(
             arquivo.name,
             tipo_arquivo,
             tamanho_kb
)

            if arquivo.name.endswith(".csv"):
                df = pd.read_csv(arquivo)
            elif arquivo.name.endswith(".xlsx"):
                df = pd.read_excel(arquivo)
            elif arquivo.name.endswith(".json"):
                df = pd.read_json(arquivo)
            else:
                df = pd.read_csv(arquivo, sep="\t")

            fim = time.time()
            tempo_ms = (fim - inicio) * 1000

            registrar_performance(
                "Carregamento de arquivo",
                tempo_ms,
                "SUCESSO"
            )

            registrar_log(
                "INFO",
                "UPLOAD",
                f"Arquivo carregado com sucesso: {arquivo.name}"
            )

            return df

        except Exception as e:
            fim = time.time()
            tempo_ms = (fim - inicio) * 1000

            registrar_performance(
                "Carregamento de arquivo",
                tempo_ms,
                "ERRO"
            )

            registrar_erro(
                "UPLOAD",
                type(e).__name__,
                str(e)
            )

            st.error(f"Erro ao ler arquivo: {e}")
            return None

    return None


def exibir_dados(df):
    if df is not None:
        st.write("### Prévia dos Dados")
        st.dataframe(df.head(10))
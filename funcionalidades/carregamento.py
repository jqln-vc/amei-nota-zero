import streamlit as st
import pandas as pd

def carregar_arquivo():
    arquivo = st.file_uploader("Arraste ou selecione seu arquivo de avaliações", type=["csv", "xlsx", "txt", "json"])
    if arquivo is not None:
        try:
            if arquivo.name.endswith('.csv'):
                return pd.read_csv(arquivo)
            elif arquivo.name.endswith('.xlsx'):
                return pd.read_excel(arquivo)
            elif arquivo.name.endswith('.json'):
                return pd.read_json(arquivo)
            else:
                return pd.read_csv(arquivo, sep='\t')
        except Exception as e:
            st.error(f"Erro ao ler arquivo: {e}")
            return None
    return None

def exibir_dados(df):
    if df is not None:
        st.write("### Prévia dos Dados")
        st.dataframe(df.head(10))
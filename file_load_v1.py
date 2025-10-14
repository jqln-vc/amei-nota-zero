import streamlit as st
import pandas as pd
import os
import fitz  # PyMuPDF


def carregar_arquivo(arquivo):
    nome = arquivo.name
    ext = os.path.splitext(nome)[1].lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(arquivo)
        elif ext == ".xlsx":
            df = pd.read_excel(arquivo)
        elif ext == ".txt":
            df = pd.DataFrame({"Texto": arquivo.read().decode("utf-8").splitlines()})
        elif ext == ".json":
            df = pd.read_json(arquivo)
        elif ext == ".pdf":
            texto = ""
            with fitz.open(stream=arquivo.read(), filetype="pdf") as doc:
                for pagina_pdf in doc:
                    texto += pagina_pdf.get_text()
            linhas = [linha for linha in texto.split("\n") if linha.strip()]
            df = pd.DataFrame({"Texto": linhas})
        else:
            st.error("Formato de arquivo não suportado.")
            return None
        st.session_state["df_avaliacoes"] = df
        return df
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
        return None


def exibir_dados(df):
    st.success("✅ Arquivo carregado com sucesso!")
    st.write("Visualização dos dados enviados:")
    st.dataframe(df.head())

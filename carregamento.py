import streamlit as st
import pandas as pd
import os
from estilos.visual import cor_texto_tema

def mostrar_erro_personalizado(modo_tema: str, mensagem: str):
    cor = cor_texto_tema(modo_tema)
    html = f"""
    <div style='color:{cor}; font-size:120%; border-left: 6px solid #FF6F61; padding: 0.5em 0.75em; margin: 0.5em 0; background-color: transparent;'>
        ⚠️ {mensagem}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def carregar_arquivo(arquivo):
    nome = arquivo.name
    ext = os.path.splitext(nome)[1].lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(arquivo)
        elif ext == ".xlsx":
            df = pd.read_excel(arquivo)
        elif ext == ".txt":
            linhas = arquivo.read().decode("utf-8").splitlines()
            df = pd.DataFrame({"Texto": linhas})
        elif ext == ".json":
            df = pd.read_json(arquivo)
        else:
            modo_tema = st.session_state.get("modo_tema", "claro")
            mostrar_erro_personalizado(modo_tema, "Formato de arquivo não suportado.")
            return None

        st.session_state["df_avaliacoes"] = df
        return df

    except Exception as e:
        modo_tema = st.session_state.get("modo_tema", "claro")
        mostrar_erro_personalizado(modo_tema, f"Erro ao processar o arquivo: {e}")
        return None

def exibir_dados(df):
    modo_tema = st.session_state.get("modo_tema", "claro")
    cor = cor_texto_tema(modo_tema)

    st.markdown(f"<p style='color:{cor}; font-size:120%;'>Visualização dos dados enviados:</p>", unsafe_allow_html=True)
    st.dataframe(df.head())

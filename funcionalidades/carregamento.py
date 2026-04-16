import streamlit as st
import pandas as pd
import os
import requests
from estilos.visual import cor_texto_tema

def mostrar_erro_personalizado(modo_tema, mensagem):
    cor = cor_texto_tema(modo_tema)
    html = f"""
    <div style='color:{cor}; font-size:120%; border-left: 6px solid #FF6F61; padding: 0.5em 0.75em; margin: 0.5em 0; background-color: transparent;'>
        ▲ {mensagem}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def carregar_arquivo(arquivo):
    if arquivo is None:
        return None
        
    nome = arquivo.name
    ext = os.path.splitext(nome)[1].lower()
    modo_tema = st.session_state.get("modo_tema", "Claro")
    
    try:
        if ext == ".csv":
            df = pd.read_csv(arquivo)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(arquivo)
        elif ext == ".txt":
            linhas = arquivo.read().decode("utf-8").splitlines()
            df = pd.DataFrame({"Texto": linhas})
        elif ext == ".json":
            df = pd.read_json(arquivo)
        else:
            mostrar_erro_personalizado(modo_tema, "Formato de arquivo não suportado.")
            return None

        # Sincronização com o Backend Flask
        url_backend = "https://amei-nota-zero.vercel.app/api/analise"
        try:
            # Envia apenas os primeiros 100 registros para evitar payload muito grande no Vercel
            payload = {"avaliacoes": df.head(100).to_dict(orient="records")}
            requests.post(url_backend, json=payload, timeout=5)
        except Exception:
            # Falha silenciosa: se o backend falhar, o app continua funcionando localmente
            pass

        st.session_state["df_avaliacoes"] = df
        return df

    except Exception as e:
        mostrar_erro_personalizado(modo_tema, f"Erro ao processar o arquivo: {str(e)}")
        return None

def exibir_dados(df):
    if df is not None:
        modo_tema = st.session_state.get("modo_tema", "Claro")
        cor = cor_texto_tema(modo_tema)
        st.markdown(f"<p style='color:{cor}; font-size:120%;'>Visualização dos dados enviados:</p>", unsafe_allow_html=True)
        st.dataframe(df.head())
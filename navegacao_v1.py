import streamlit as st


def configurar_navegacao():
    return st.sidebar.radio("Navegação", [
        "Início",
        "Análise de Sentimento",
        "Tópicos Relevantes",
        "Resumo de Insights",
        "Visualização de Dados",
        "Relatório Final"
    ])

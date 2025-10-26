import streamlit as st
from estilos.visual import cor_texto_tema

def configurar_navegacao():
    modo_tema = st.session_state.get("modo_tema", "claro")
    cor = cor_texto_tema(modo_tema)

    st.sidebar.markdown(
        f"<p style='color:{cor}; font-size:120%; font-weight:500;'>Navegação</p>",
        unsafe_allow_html=True
    )

    return st.sidebar.radio(
        label="",
        options=["Início", "Análise de Avaliações", "Relatório Final"]
    )

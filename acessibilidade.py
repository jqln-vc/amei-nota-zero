import streamlit as st
from visual import cor_texto_tema

def configurar_acessibilidade():
    # Define tema padrão se ainda não estiver definido
    if "modo_tema" not in st.session_state:
        st.session_state.modo_tema = "Claro"

    modo_tema = st.session_state.modo_tema
    cor = cor_texto_tema(modo_tema)

    # Título da seção com estilo adaptativo
    st.sidebar.markdown(
        f"<h3 style='color:{cor}; font-size:120%;'>♿ Acessibilidade Visual</h3>",
        unsafe_allow_html=True
    )

    # Tema visual
    st.sidebar.markdown(
        f"<p style='color:{cor}; font-size:120%; font-weight:500;'>Tema visual:</p>",
        unsafe_allow_html=True
    )
    modo_tema = st.sidebar.radio(
        label="",
        options=["Claro", "Escuro"],
        index=0 if st.session_state.modo_tema == "Claro" else 1
    )
    st.session_state.modo_tema = modo_tema

    # Tamanho da fonte
    st.sidebar.markdown(
        f"<p style='color:{cor}; font-size:120%; font-weight:500;'>🔠 Tamanho da fonte:</p>",
        unsafe_allow_html=True
    )
    tamanho_fonte = st.sidebar.radio(
        label="",
        options=["Padrão", "Grande", "Extra Grande"]
    )

    return modo_tema, tamanho_fonte

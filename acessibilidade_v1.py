import streamlit as st


def configurar_acessibilidade():
    st.sidebar.markdown("### ♿ Acessibilidade Visual")


    if "modo_tema" not in st.session_state:
        st.session_state.modo_tema = "Claro"


    modo_tema = st.sidebar.radio(
        "Tema visual:",
        ["Claro", "Escuro"],
        index=0 if st.session_state.modo_tema == "Claro" else 1
    )
    st.session_state.modo_tema = modo_tema


    tamanho_fonte = st.sidebar.radio(
        "🔠 Tamanho da fonte:",
        ["Padrão", "Grande", "Extra Grande"]
    )


    return modo_tema, tamanho_fonte

import streamlit as st
from estilos.visual import cor_texto_tema

def configurar_navegacao():
    modo_tema = st.session_state.get("modo_tema", "Claro")
    cor = cor_texto_tema(modo_tema)
    
    if "pagina_atual" not in st.session_state:
        st.session_state.pagina_atual = "Início"

    st.sidebar.markdown(
        f"<p style='color:{cor}; font-size:125%; font-weight:600; margin-top:10px;'>🗺️ Navegação</p>",
        unsafe_allow_html=True
    )

    # Definindo cores para o botão inativo com base no tema
    if modo_tema.lower() == "escuro":
        fundo_inativo = "rgba(255, 255, 255, 0.05)"
        cor_texto_inativo = "#FFFFFF"
        borda_inativa = "rgba(255, 255, 255, 0.2)"
    else:
        fundo_inativo = "rgba(0, 0, 0, 0.05)"
        cor_texto_inativo = "#222222"
        borda_inativa = "rgba(0, 0, 0, 0.1)"

    estilo_botoes = f"""
    <style>
        /* Estilo base para os botões da sidebar */
        div[data-testid="stSidebarUserContent"] .stButton > button {{
            width: 100%;
            border-radius: 8px;
            text-align: left;
            padding: 10px 15px;
            margin-bottom: -5px;
            display: flex;
            justify-content: flex-start;
            transition: all 0.2s ease;
        }}

        /* Ajuste específico para botões secundários (Inativos) */
        div[data-testid="stSidebarUserContent"] .stButton > button[kind="secondary"] {{
            background-color: {fundo_inativo} !important;
            color: {cor_texto_inativo} !important;
            border: 1px solid {borda_inativa} !important;
        }}

        /* Efeito de hover para botões inativos */
        div[data-testid="stSidebarUserContent"] .stButton > button[kind="secondary"]:hover {{
            border-color: #009688 !important;
            color: #009688 !important;
            background-color: transparent !important;
        }}
    </style>
    """
    st.sidebar.markdown(estilo_botoes, unsafe_allow_html=True)

    if st.sidebar.button("**Início**", key="nav_inicio", use_container_width=True,
                         type="primary" if st.session_state.pagina_atual == "Início" else "secondary"):
        st.session_state.pagina_atual = "Início"
        st.rerun()

    if st.sidebar.button("**Análise de Avaliações**", key="nav_analise", use_container_width=True,
                         type="primary" if st.session_state.pagina_atual == "Análise de Avaliações" else "secondary"):
        st.session_state.pagina_atual = "Análise de Avaliações"
        st.rerun()

    return st.session_state.pagina_atual
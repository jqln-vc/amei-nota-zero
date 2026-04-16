import streamlit as st
from estilos.visual import cor_texto_tema

def configurar_acessibilidade():
    if "modo_tema" not in st.session_state:
        st.session_state.modo_tema = "Claro"
    if "tamanho_fonte" not in st.session_state:
        st.session_state.tamanho_fonte = "Padrão"

    modo_tema = st.session_state.modo_tema
    tamanho_fonte = st.session_state.tamanho_fonte
    cor = cor_texto_tema(modo_tema)

    # Injeção de CSS para garantir negrito nos botões da sidebar
    st.sidebar.markdown("""
        <style>
            div[data-testid="stSidebarUserContent"] .stButton > button p {
                font-weight: bold !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(
        f"<p style='color:{cor}; font-size:125%; font-weight:bold; margin-top:20px;'>♿ Acessibilidade Visual</p>",
        unsafe_allow_html=True
    )

    # 1. Escolha de Tema (Lado a lado)
    st.sidebar.markdown(f"<p style='color:{cor}; font-size:90%; font-weight:bold; margin-bottom:5px;'>Tema visual:</p>", unsafe_allow_html=True)
    col_t1, col_t2 = st.sidebar.columns(2)
    
    if col_t1.button("**Claro ☀️**", key="btn_claro", use_container_width=True, 
                   type="primary" if modo_tema == "Claro" else "secondary"):
        st.session_state.modo_tema = "Claro"
        st.rerun()
            
    if col_t2.button("**Escuro 🌙**", key="btn_escuro", use_container_width=True, 
                   type="primary" if modo_tema == "Escuro" else "secondary"):
        st.session_state.modo_tema = "Escuro"
        st.rerun()

    # 2. Escolha de Tamanho da Fonte (Vertical)
    st.sidebar.markdown(f"<p style='color:{cor}; font-size:90%; font-weight:bold; margin-top:10px; margin-bottom:5px;'>Tamanho da fonte:</p>", unsafe_allow_html=True)
    
    opcoes = ["Padrão", "Grande", "Extra Grande"]
    for op in opcoes:
        # Define se o botão deve estar em destaque (Primary) ou normal (Secondary)
        estilo_botao = "primary" if tamanho_fonte == op else "secondary"
        
        if st.sidebar.button(f"**{op}**", key=f"f_size_{op}", use_container_width=True, type=estilo_botao):
            st.session_state.tamanho_fonte = op
            st.rerun()

    return st.session_state.modo_tema, st.session_state.tamanho_fonte
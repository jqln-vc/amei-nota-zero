import streamlit as st

def aplicar_estilos(tamanho_fonte, modo_tema):
    tamanhos = {
        "Padrão": "16px",
        "Grande": "18px",
        "Extra Grande": "22px"
    }
    fonte = tamanhos.get(tamanho_fonte, "16px")

    # Verifica se é modo claro
    is_claro = modo_tema.strip().lower() == "claro"

    if is_claro:
        cor_texto = "#222222"
        fundo_geral = "#ffffff"
        fundo_sidebar = "#f9f9f9"
        cor_acao_primaria = "#009688"
        fundo_upload = "#F0F2F6"
        fundo_botao_secundario = "#ffffff"
        borda_botao_secundario = "#dcdcdc"
    else:
        # MODO ESCURO
        cor_texto = "#FFFFFF"
        fundo_geral = "#0E1117"
        fundo_sidebar = "#161B22"
        cor_acao_primaria = "#009688"
        fundo_upload = "#1E1E1E"
        fundo_botao_secundario = "#262730"
        borda_botao_secundario = "#444444"

    st.session_state["cor_texto_dinamico"] = cor_texto

    css = f"""
    <style>
    /* 1. CONFIGURAÇÃO GERAL DE TEXTO E FUNDO */
    html, body, [class*="css"], .stApp {{
        font-size: {fonte} !important;
        background-color: {fundo_geral} !important;
        color: {cor_texto} !important;
    }}

    /* 2. FORÇAR CORES EM TÍTULOS E TEXTOS BASES */
    h1, h2, h3, h4, h5, h6, p, span, label {{
        color: {cor_texto} !important;
    }}

    /* 3. SIDEBAR (MENU LATERAL) */
    section[data-testid="stSidebar"] {{
        background-color: {fundo_sidebar} !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {{
        color: {cor_texto} !important;
    }}

    /* 4. ÁREA DE UPLOAD (CORREÇÃO DE CONTRASTE) */
    [data-testid="stFileUploaderDropzone"] {{
        background-color: {fundo_upload} !important;
        border: 2px dashed {cor_acao_primaria}44 !important;
    }}
    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] svg {{
        color: {cor_texto} !important;
    }}
    [data-testid="stFileUploaderDropzone"] small {{
        color: {cor_texto} !important;
        opacity: 0.8;
    }}
    [data-testid="stFileUploaderDropzone"] button {{
        background-color: {cor_acao_primaria} !important;
        color: white !important;
        border: none !important;
    }}

    /* 5. BOTÕES (CORREÇÃO DEFINITIVA DO TEMA) */
    /* Botão Primário (Ativo) */
    .stButton > button[kind="primary"] {{
        background-color: {cor_acao_primaria} !important;
        color: white !important;
        border: none !important;
    }}
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span {{
        color: white !important;
    }}

    /* Botão Secundário (Inativo) */
    .stButton > button[kind="secondary"] {{
        background-color: {fundo_botao_secundario} !important;
        color: {cor_texto} !important;
        border: 1px solid {borda_botao_secundario} !important;
    }}
    .stButton > button[kind="secondary"] p,
    .stButton > button[kind="secondary"] span {{
        color: {cor_texto} !important;
    }}
    /* Efeito Hover no botão secundário */
    .stButton > button[kind="secondary"]:hover {{
        border-color: {cor_acao_primaria} !important;
        color: {cor_acao_primaria} !important;
    }}
    .stButton > button[kind="secondary"]:hover p,
    .stButton > button[kind="secondary"]:hover span {{
        color: {cor_acao_primaria} !important;
    }}

    /* 6. MÉTRICAS (CARTÕES DE NÚMEROS) */
    [data-testid="stMetricLabel"] p {{
        color: {cor_texto} !important;
    }}
    [data-testid="stMetricValue"] div {{
        color: {cor_texto} !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def obter_paleta(modo_tema):
    return {
        "Elogios": "#009E73",
        "Sugestões": "#E69F00",
        "Criticas": "#D55E00"
    }

def cor_texto_tema(modo_tema):
    return "#222222" if modo_tema.strip().lower() == "claro" else "#FFFFFF"

def mostrar_aviso(mensagem, modo_tema):
    """Gera um aviso minimalista com barra lateral vermelha conforme a referência."""
    cor_txt = cor_texto_tema(modo_tema)
    st.markdown(f"""
    <div style='border-left: 4px solid #FF4B4B; padding-left: 15px; margin: 25px 0 15px 0; line-height: 1.6;'>
        <span style='color: {cor_txt}; font-size: 1.1em; font-weight: 400;'>{mensagem}</span>
    </div>
    """, unsafe_allow_html=True)
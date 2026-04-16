import streamlit as st

def aplicar_estilos(tamanho_fonte, modo_tema):
    tamanhos = {
        "Padrão": "16px",
        "Grande": "18px",
        "Extra Grande": "22px"
    }
    fonte = tamanhos.get(tamanho_fonte, "16px")

    if modo_tema.strip().lower() == "claro":
        cor_texto = "#222222"
        fundo_geral = "#ffffff"
        fundo_sidebar = "#f9f9f9"
        cor_acao_primaria = "#009688"
        fundo_upload = "#F0F2F6"
    else:
        # MODO ESCURO
        cor_texto = "#FFFFFF"
        fundo_geral = "#0E1117"
        fundo_sidebar = "#161B22"
        cor_acao_primaria = "#009688"
        fundo_upload = "#1E1E1E"

    st.session_state["cor_texto_dinamico"] = cor_texto

    css = f"""
    <style>
    /* 1. CONFIGURAÇÃO GERAL DE TEXTO E FUNDO */
    html, body, [class*="css"], .stApp {{
        font-size: {fonte} !important;
        background-color: {fundo_geral} !important;
        color: {cor_texto} !important;
    }}

    /* 2. FORÇAR CORES EM TÍTULOS, SUBTÍTULOS E PARÁGRAFOS */
    h1, h2, h3, h4, h5, h6, p, span, label {{
        color: {cor_texto} !important;
    }}

    /* 3. MÉTRICAS (CARTÕES DE NÚMEROS) */
    [data-testid="stMetricLabel"] p {{
        color: {cor_texto} !important;
    }}
    [data-testid="stMetricValue"] div {{
        color: {cor_texto} !important;
    }}

    /* 4. SIDEBAR (MENU LATERAL) */
    section[data-testid="stSidebar"] {{
        background-color: {fundo_sidebar} !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {{
        color: {cor_texto} !important;
    }}

    /* 5. ÁREA DE UPLOAD (CORREÇÃO DE CONTRASTE) */
    [data-testid="stFileUploaderDropzone"] {{
        background-color: {fundo_upload} !important;
        border: 2px dashed {cor_acao_primaria}44 !important;
    }}
    /* Texto principal e ícone */
    [data-testid="stFileUploaderDropzone"] p, 
    [data-testid="stFileUploaderDropzone"] svg {{
        color: {cor_texto} !important;
    }}
    /* Texto pequeno (formatos e limite de tamanho) */
    [data-testid="stFileUploaderDropzone"] small {{
        color: {cor_texto} !important;
        opacity: 0.8;
    }}
    /* Botão interno 'Browse files' */
    [data-testid="stFileUploaderDropzone"] button {{
        background-color: {cor_acao_primaria} !important;
        color: white !important;
        border: none !important;
    }}

    /* 6. BOTÕES DA SIDEBAR - ESTADO ATIVO */
    div[data-testid="stSidebarUserContent"] .stButton > button[kind="primary"] {{
        background-color: {cor_acao_primaria} !important;
        color: white !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def obter_paleta(modo_tema):
    return {
        "Elogios": "#009E73",
        "Sugestões": "#E69F00",
        "Críticas": "#D55E00"
    }

def cor_texto_tema(modo_tema):
    return "#222222" if modo_tema.strip().lower() == "claro" else "#FFFFFF"

def mostrar_aviso(modo_tema):
    cor_txt = cor_texto_tema(modo_tema)
    st.markdown(f"""
        <div style='border-left: 6px solid #FFB300; padding: 12px; background: rgba(255,179,0,0.1); color: {cor_txt}; margin: 10px 0;'>
            <strong>AVISO:</strong> Por favor, envie um arquivo na aba <strong>'Início'</strong> para acessar a análise.
        </div>
    """, unsafe_allow_html=True)
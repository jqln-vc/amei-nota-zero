import streamlit as st

def aplicar_estilos(tamanho_fonte: str, modo_tema: str):
    tamanhos = {
        "Padrão": "16px",
        "Grande": "18px",
        "Extra Grande": "22px"
    }
    fonte = tamanhos.get(tamanho_fonte, "16px")

    if modo_tema.strip().lower() == "claro":
        cor_titulo = "#222222"
        fundo_geral = "#ffffff"
        fundo_sidebar = "#f9f9f9"
        cor_texto_aviso = "#5D4037"
        cor_borda_aviso = "#FFD54F"
    else:
        cor_titulo = "#e0e0e0"
        fundo_geral = "#121212"
        fundo_sidebar = "#1e1e1e"
        cor_texto_aviso = "#FFECB3"
        cor_borda_aviso = "#FFB300"

    st.session_state["cor_texto_dinamico"] = cor_titulo

    css = f"""
    <style>
        html, body, [class*="css"] {{
            font-size: {fonte} !important;
            background-color: {fundo_geral} !important;
            color: {cor_titulo} !important;
        }}
        .stApp {{
            background-color: {fundo_geral} !important;
            color: {cor_titulo} !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {fundo_sidebar} !important;
        }}
        section[data-testid="stSidebar"] * {{
            color: {cor_titulo} !important;
            font-size: 103% !important;
        }}

        .markdown-text-container p,
        .markdown-text-container li,
        .stCaption,
        .stMarkdown,
        .upload-box,
        .titulo-upload,
        .stDataFrame,
        .stTable {{
            font-size: 120% !important;
        }}
        h1, h2, h3, h4 {{
            font-size: revert !important;
        }}

        div[data-testid="stFileUploader"] *,
        div[data-testid="stFileUploader"] > div {{
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0px !important;
            margin: 0px !important;
            color: {cor_titulo} !important;
        }}

        div[data-testid="stFileUploader"] span {{
            color: {cor_titulo} !important;
        }}

        input[type="file"] {{
            background-color: transparent !important;
            color: {cor_titulo} !important;
        }}

        div[class*="stAlert"],
        div[class*="stMarkdown"],
        div[data-testid="stMarkdownContainer"] {{
            background-color: transparent !important;
            box-shadow: none !important;
            border: none !important;
            padding: 0px !important;
            margin: 0px !important;
        }}

        .titulo-upload {{
            color: {cor_titulo} !important;
            font-size: 20px !important;
            font-weight: 600;
            margin-bottom: 0.5em;
        }}
        .upload-box {{
            max-width: 500px;
            margin-bottom: 1em;
            color: {cor_titulo} !important;
        }}

        .aviso-custom {{
            background-color: transparent !important;
            color: {cor_texto_aviso} !important;
            border-left: 6px solid {cor_borda_aviso} !important;
            font-size: 120% !important;
            margin: 0.5em 0 !important;
            padding: 0.5em 0.75em !important;
            box-shadow: none !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def mostrar_aviso(modo_tema: str):
    html = """
    <div class="aviso-custom">
        <strong>AVISO:</strong> Nenhum arquivo foi carregado ainda. Por favor, envie um arquivo na aba <strong>'Início'</strong> para gerar o relatório.
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def mostrar_erro_personalizado(modo_tema: str, mensagem: str):
    cor = cor_texto_tema(modo_tema)
    html = f"""
    <div style='color:{cor}; font-size:120%; border-left: 6px solid #FF6F61; padding: 0.5em 0.75em; margin: 0.5em 0; background-color: transparent; box-shadow: none;'>
        <strong>AVISO:</strong> {mensagem}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def obter_paleta(modo_tema: str) -> dict:
    return {
        "positive": "#009E73",     # Verde petróleo — seguro para daltonismo
        "neutral": "#E69F00",   # Laranja queimado — alto contraste
        "negative": "#D55E00"     # Vermelho escuro — perceptível mesmo com protanopia
    }

def cor_texto_tema(modo_tema: str) -> str:
    return "#222222" if modo_tema.strip().lower() == "claro" else "#e0e0e0"

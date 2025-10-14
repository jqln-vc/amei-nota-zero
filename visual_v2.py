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
        }}


        /* Zera tudo no uploader */
        div[data-testid="stFileUploader"] *,
        div[data-testid="stFileUploader"] > div {{
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0px !important;
            margin: 0px !important;
            color: {cor_titulo} !important;
        }}


        /* Texto do uploader */
        div[data-testid="stFileUploader"] span {{
            color: {cor_titulo} !important;
        }}


        input[type="file"] {{
            background-color: transparent !important;
            color: {cor_titulo} !important;
        }}


        /* Remove fundo dos blocos de markdown e alertas */
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


        /* Estilo do aviso adaptável */
        .aviso-custom {{
            background-color: transparent !important;
            color: {cor_texto_aviso} !important;
            border-left: 6px solid {cor_borda_aviso} !important;
            font-size: 16px !important;
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
        ⚠️ Nenhum arquivo foi carregado ainda. Por favor, envie um arquivo na aba <strong>'Início'</strong> para gerar o relatório.
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def obter_paleta(modo_tema: str) -> dict:
    if modo_tema.strip().lower() == "claro":
        base = {
            "Positivo": "#2E7D32",
            "Neutro": "#FBC02D",
            "Negativo": "#C62828"
        }
    else:
        base = {
            "Positivo": "#4CAF50",
            "Neutro": "#FFC107",
            "Negativo": "#F44336"
        }


    return {
        "Positivo": base["Positivo"],
        "Neutro": base["Neutro"],
        "Negativo": base["Negativo"],
        "Elogios": base["Positivo"],
        "Sugestões": base["Neutro"],
        "Críticas": base["Negativo"]
    }

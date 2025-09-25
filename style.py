import streamlit as st


def aplicar_estilos(tamanho):
    if tamanho == "Padrão":
        tamanho_css = "16px"
        padding_css = "0.5em 1em"
    elif tamanho == "Grande":
        tamanho_css = "20px"
        padding_css = "0.75em 1.5em"
    elif tamanho == "Extra Grande":
        tamanho_css = "24px"
        padding_css = "1em 2em"
    else:
        tamanho_css = "16px"
        padding_css = "0.5em 1em"


    st.markdown(f"""
        <style>
        html, body, [class*="css"] {{
            font-size: {tamanho_css};
        }}
        button, .stButton > button {{
            font-size: {tamanho_css} !important;
            padding: {padding_css} !important;
        }}
        .stRadio > div {{
            font-size: {tamanho_css};
        }}
        </style>
    """, unsafe_allow_html=True)


def obter_paleta(tema="Claro"):
    return {
        "Positivo": "#2ECC71",
        "Neutro": "#F8CAA0",
        "Negativo": "#E74C3C",
        "Elogios": "#2ECC71",
        "Sugestões": "#F8CAA0",
        "Críticas": "#E74C3C"
    }

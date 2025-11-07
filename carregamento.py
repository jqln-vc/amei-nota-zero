import streamlit as st
import pandas as pd
import os
import io
import json
import tempfile
from fpdf import FPDF
from fpdf.enums import Align
import altair as alt
import vl_convert as vlc
import sqlite3
from visual import cor_texto_tema

def mostrar_erro_personalizado(modo_tema: str, mensagem: str):
    cor = cor_texto_tema(modo_tema)
    html = f"""
    <div style='color:{cor}; font-size:120%; border-left: 6px solid #FF6F61; padding: 0.5em 0.75em; margin: 0.5em 0; background-color: transparent;'>
        ⚠️ {mensagem}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def carregar_arquivo(arquivo):
    nome = arquivo.name
    ext = os.path.splitext(nome)[1].lower()
    column_data = [
    "name",
    "review_text",
    "reviews_per_score_1",
    "reviews_per_score_2",
    "reviews_per_score_3",
    "reviews_per_score_4",
    "reviews_per_score_5"
    ]
    try:
        if ext == ".csv":
            df = pd.read_csv(arquivo)
        elif ext == ".xlsx":
            df = pd.read_excel(arquivo)
        elif ext == ".txt":
            linhas = arquivo.read().decode("utf-8").splitlines()
            df = pd.DataFrame({"Texto": linhas})
        elif ext == ".json":
            data = json.load(arquivo)
            df = pd.DataFrame(data, columns=column_data)
        else:
            modo_tema = st.session_state.get("modo_tema", "claro")
            mostrar_erro_personalizado(modo_tema, "Formato de arquivo não suportado.")
            return None

        
        return df

    except Exception as e:
        modo_tema = st.session_state.get("modo_tema", "claro")
        mostrar_erro_personalizado(modo_tema, f"Erro ao processar o arquivo: {e}")
        return None

def exibir_dados(df):
    modo_tema = st.session_state.get("modo_tema", "claro")
    cor = cor_texto_tema(modo_tema)

    st.markdown(f"<p style='color:{cor}; font-size:120%;'>Visualização dos dados enviados:</p>", unsafe_allow_html=True)
    st.dataframe(df.head(100))

def gerar_relatorio(company: str, sent_chart: alt.Chart, key_topics: list, summary: str, advice: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Relatório de Análise de Avaliações de {company}", ln=True, align=Align.C)

    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "Tópicos Principais:", ln=True)
    pdf.set_font("Helvetica", '', 12)
    for topic in key_topics:
        pdf.multi_cell(0, 10, f"- {topic}")

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "Resumo das Avaliações:", ln=True)
    pdf.set_font("Helvetica", '', 12)
    pdf.multi_cell(0, 10, summary)

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "Recomendações:", ln=True)
    pdf.set_font("Helvetica", '', 12)
    pdf.multi_cell(0, 10, advice)


    png_bytes = vlc.vegalite_to_png(
        sent_chart.to_dict(),
        scale=2, 
    )

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        tmp_file.write(png_bytes)
        temp_file_path = tmp_file.name # Get the actual file path
    
    # Adicionar gráfico ao PDF
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Gráfico de Análise de Sentimento:", ln=True)
    pdf.image(temp_file_path, type='PNG', x=10, y=None, w=pdf.w - 30)
    os.remove(temp_file_path)
    

    return pdf.output(dest='S').encode('latin-1')

# 1. Função para conectar e cachear o objeto de conexão
@st.cache_resource
def conectar_banco():
    conn = st.connection(
        name="database_connection", 
        type="sql",
        url="sqlite:///avaliacoes.db"
    )
    return conn


# 2. Exemplo de uso para salvar o DataFrame
def salvar_avaliacoes(df, conn):
    try:
        df.to_sql(
            name="avaliacoes", 
            con=conn.engine, # Usar o .engine do objeto st.connection
            if_exists="replace", 
            index=False
        )

        st.success("Dados salvos com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")

# Exemplo de uso para ler o DataFrame
def carregar_avaliacoes(conn):
    return conn.query("SELECT * FROM avaliacoes")
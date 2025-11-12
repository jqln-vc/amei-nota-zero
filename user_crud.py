import sqlite3
import streamlit as st
import pandas as pd

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
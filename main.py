import streamlit as st
from componentes.layout import construir_interface

if "config_executada" not in st.session_state:
    st.session_state.config_executada = True

if __name__ == "__main__":
    construir_interface()
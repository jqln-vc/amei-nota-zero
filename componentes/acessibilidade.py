import streamlit as st

def construir_acessibilidade():
    st.markdown("### ♿ Acessibilidade Visual")
    
    # Seletor de Tema
    st.write("**Tema visual:**")
    col1, col2 = st.columns(2)
    
    with col1:
        tipo = "primary" if st.session_state.get("modo_tema") == "Claro" else "secondary"
        if st.button("Claro ☀️", key="btn_claro", type=tipo, use_container_width=True):
            st.session_state["modo_tema"] = "Claro"
            st.rerun()
            
    with col2:
        tipo = "primary" if st.session_state.get("modo_tema") == "Escuro" else "secondary"
        if st.button("Escuro 🌙", key="btn_escuro", type=tipo, use_container_width=True):
            st.session_state["modo_tema"] = "Escuro"
            st.rerun()

    # Tamanho da fonte
    st.write("**Tamanho da fonte:**")
    opcoes = ["Padrão", "Grande", "Extra Grande"]
    
    # Criar botões verticais para o tamanho
    for opcao in opcoes:
        tipo = "primary" if st.session_state.get("tamanho_fonte", "Padrão") == opcao else "secondary"
        if st.button(opcao, key=f"btn_{opcao}", type=tipo, use_container_width=True):
            st.session_state["tamanho_fonte"] = opcao
            st.rerun()
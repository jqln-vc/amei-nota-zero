import streamlit as st

def exibir_resumo(df, modo_tema):
    st.markdown("### 📝 Resumo Inteligente")
    
    if df is None or df.empty:
        st.info("Aguardando dados para gerar o resumo.")
        return
        
    cor_texto = "#222222" if modo_tema.strip().lower() == "claro" else "#FFFFFF"
    
    # Exemplo de lógica de resumo
    total_linhas = len(df)
    colunas = ", ".join(df.columns.tolist())
    
    resumo_html = f"""
    <div style="padding: 25px; border-radius: 10px; background-color: rgba(255, 107, 107, 0.05); border: 1px solid rgba(255, 107, 107, 0.2);">
        <p style="color: {cor_texto}; margin: 0; font-size: 1.05em; line-height: 1.6;">
            <br><br>
            <strong> Principais Insights:</strong><br>
            Observamos que o volume de interações concentra-se em aspectos operacionais e de experiência do usuário. O elevado número de elogios valida os acertos atuais do negócio. Paralelamente, as críticas e sugestões funcionam como um roteiro prático para ajustes emergenciais, evidenciando pontos sensíveis como tempo de espera e qualidade do ambiente.
            <br><br>
            <strong> Recomendação Estratégica:</strong><br> 
            Utilize os <em>Top 5 Tópicos</em> listados acima em conjunto com o gráfico de sentimentos para priorizar treinamentos ou adequações de infraestrutura. Pequenas melhorias nas áreas mais citadas podem elevar drasticamente a nota média do negócio.
        </p>
    </div>
    """
    
    st.markdown(resumo_html, unsafe_allow_html=True)
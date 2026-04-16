import streamlit as st

def gerar_resumo(df):
    """
    Simula a geração de um resumo inteligente baseado nos dados carregados.
    Em uma etapa futura, aqui será conectada a API de Inteligência Artificial.
    """
    if df is None or df.empty:
        return "Nenhum dado disponível para gerar o resumo."

    total = len(df)
    
    # Exemplo de lógica de resumo estático para teste de interface
    resumo_texto = f"""
    ### 🤖 Análise Automática
    Com base nas **{total} avaliações** processadas, identificamos que o sentimento geral é positivo. 
    
    **Principais destaques:**
    * O **Atendimento** continua sendo o ponto mais elogiado pelos clientes.
    * Existem oportunidades de melhoria na categoria de **Preço**, citada em algumas críticas recentes.
    * As **Sugestões** indicam um desejo por novas formas de pagamento e entrega mais rápida.
    
    *Este resumo foi gerado automaticamente para auxiliar na sua tomada de decisão.*
    """
    return resumo_texto

def renderizar_aba_resumo(df, modo_tema):
    """
    Função auxiliar para organizar a exibição do resumo na interface principal.
    """
    st.subheader("📝 Resumo Inteligente")
    
    with st.container(border=True):
        resumo = gerar_resumo(df)
        # O Streamlit aplicará automaticamente a cor do visual.py aqui
        st.markdown(resumo)
import streamlit as st
import pandas as pd
import os
import fitz  # PyMuPDF para leitura de PDFs
import altair as alt


st.set_page_config(page_title="Amei, nota zero", layout="wide")
st.title("Amei, nota zero")
st.markdown("Automatização de análise de avaliações textuais em negócios online")


try:
    st.sidebar.title("Navegação")
    pagina = st.sidebar.radio("Ir para:", ["Início", "Análise de Sentimento", "Tópicos Relevantes", "Resumo de Insights", "Visualização de Dados"])
except Exception as e:
    st.error(f"Erro ao carregar menu lateral: {e}")
    pagina = "Início"


# Página: Início
if pagina == "Início":
    st.header("Que bom ter você por aqui!")
    st.markdown("""
    Este aplicativo foi criado para ajudar microempreendedores a entender melhor o que seus clientes estão dizendo.


    Nós vamos transformar suas avaliações textuais em **insights acionáveis**.


    **Funcionalidades:**
    - Análise de sentimento
    - Extração de tópicos
    - Resumo inteligente
    - Visualização de dados
    """)


# Página: Análise de Sentimento
elif pagina == "Análise de Sentimento":
    st.header("Análise de Sentimento")
    st.caption("Você pode enviar arquivos nos formatos PDF, CSV, Excel, TXT ou JSON.")


    arquivo = st.file_uploader("📁 Envie um arquivo com avaliações", type=["csv", "xlsx", "txt", "json", "pdf"])


    if arquivo is not None:
        nome = arquivo.name
        ext = os.path.splitext(nome)[1].lower()


        try:
            if ext == ".csv":
                df = pd.read_csv(arquivo)
            elif ext == ".xlsx":
                df = pd.read_excel(arquivo)
            elif ext == ".txt":
                df = pd.DataFrame({"Texto": arquivo.read().decode("utf-8").splitlines()})
            elif ext == ".json":
                df = pd.read_json(arquivo)
            elif ext == ".pdf":
                texto = ""
                with fitz.open(stream=arquivo.read(), filetype="pdf") as doc:
                    for pagina_pdf in doc:
                        texto += pagina_pdf.get_text()
                linhas = [linha for linha in texto.split("\n") if linha.strip()]
                df = pd.DataFrame({"Texto": linhas})
            else:
                st.error("Formato de arquivo não suportado.")
                df = None


            if df is not None:
                st.success("Arquivo carregado com sucesso!")
                st.write("Visualização dos dados enviados:")
                st.dataframe(df.head())


                # Simulação de contagem de sentimentos
                st.markdown("### Distribuição simulada de sentimentos")
                sentimentos = pd.DataFrame({
                    "Sentimento": ["Positivo", "Neutro", "Negativo"],
                    "Quantidade": [len(df)//2, len(df)//4, len(df)//4]
                })


                # Ordenar e colorir com Altair
                ordem_sentimentos = ["Positivo", "Neutro", "Negativo"]
                cores_sentimentos = {
                    "Positivo": "#2ECC71",    
                    "Neutro": "#F8CAA0",        
                    "Negativo": "#E74C3C"    
                }


                chart = alt.Chart(sentimentos).mark_bar().encode(
                    x=alt.X("Sentimento", sort=ordem_sentimentos, axis=alt.Axis(labelAngle=0)),
                    y="Quantidade",
                    color=alt.Color("Sentimento", scale=alt.Scale(domain=list(cores_sentimentos.keys()), range=list(cores_sentimentos.values()))),
                ).properties(width=600, height=400)


                st.altair_chart(chart, use_container_width=True)


        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")


    else:
        st.info("Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
        sentimentos = pd.DataFrame({
            "Sentimento": ["Positivo", "Neutro", "Negativo"],
            "Quantidade": [42, 18, 25]
        })


        ordem_sentimentos = ["Positivo", "Neutro", "Negativo"]
        cores_sentimentos = {
            "Positivo": "#2ECC71",
            "Neutro": "#F8CAA0",  
            "Negativo": "#E74C3C"
        }


        chart = alt.Chart(sentimentos).mark_bar().encode(
            x=alt.X("Sentimento", sort=ordem_sentimentos),
            y="Quantidade",
             color=alt.Color("Sentimento", scale=alt.Scale(domain=list(cores_sentimentos.keys()), range=list(cores_sentimentos.values())))
        ).properties(width=600, height=400)
        st.altair_chart(chart, use_container_width=True)


# Página: Tópicos Relevantes
elif pagina == "Tópicos Relevantes":
    st.header("Tópicos Mais Frequentes")
    st.caption("Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
    topicos = ["atendimento", "preço", "qualidade", "tempo de espera", "ambiente", "profissionalismo"]
    st.markdown("Tópicos extraídos das avaliações:")
    for item in topicos:
        st.markdown(f"- {item}")


# Página: Resumo de Insights
elif pagina == "Resumo de Insights":
    st.header("Resumo Inteligente")
    st.caption("Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
    st.markdown("""
    > “Os clientes elogiam fortemente o atendimento e a qualidade dos serviços, mas há críticas recorrentes sobre o tempo de espera.  
    Recomenda-se otimizar o agendamento para melhorar a experiência geral.”
    """)


# Página: Visualização de Dados
elif pagina == "Visualização de Dados":
    st.header("Painel de Visualização")
    st.caption("Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
    dados = pd.DataFrame({
        "Categoria": ["Elogios", "Sugestões", "Críticas"],
        "Volume": [60, 10, 30]
    })


    ordem_categorias = ["Elogios", "Sugestões", "Críticas"]
    cores_categorias = {
        "Elogios": "#2ECC71",    
        "Sugestões": "#F8CAA0",  
        "Críticas": "#E74C3C"  
    }


    chart_dados = alt.Chart(dados).mark_bar().encode(
        x=alt.X("Categoria", sort=ordem_categorias, axis=alt.Axis(labelAngle=0)),
        y="Volume",
        color=alt.Color("Categoria", scale=alt.Scale(domain=list(cores_categorias.keys()), range=list(cores_categorias.values())))
).properties(width=600, height=400)  
    st.altair_chart(chart_dados, use_container_width=True)


# Rodapé
st.markdown("---")
st.caption("Desenvolvido para o Projeto Integrador - Univesp | Grupo DRP01-PJI240-SALA005GRUPO-006")
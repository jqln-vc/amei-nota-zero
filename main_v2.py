import streamlit as st
import pandas as pd
import os
import fitz  # PyMuPDF
import altair as alt
import re
from collections import Counter


# Função de estilos visuais
def aplicar_estilos(tema, tamanho_fonte):
    estilos = "<style>"


    if tema == "Claro":
        estilos += """
        .stApp {
            background-color: #FFFFFF;
            color: #31333F;
        }
        h1, h2, h3, h4, h5, h6, p, label, div, span {
            color: #31333F !important;
        }
        .css-1d391kg, .css-1cpxqw2, .css-ffhzg2, .css-1v0mbdj, .css-1y4p8pa {
            background-color: #F0F2F6 !important;
            color: #31333F !important;
        }
        """
    elif tema == "Escuro":
        estilos += """
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        h1, h2, h3, h4, h5, h6, p, label, div, span {
            color: #FFFFFF !important;
        }
        .css-1d391kg, .css-1cpxqw2, .css-ffhzg2, .css-1v0mbdj, .css-1y4p8pa {
            background-color: #2C2C2C !important;
            color: #FFFFFF !important;
        }
        """


    if tamanho_fonte == "Grande":
        estilos += """
        html, body, [class*="css"] {
            font-size: 18px !important;
        }
        """
    elif tamanho_fonte == "Extra Grande":
        estilos += """
        html, body, [class*="css"] {
            font-size: 22px !important;
        }
        """


    estilos += "</style>"
    st.markdown(estilos, unsafe_allow_html=True)


# Função para obter paleta de cores
def obter_paleta(tema):
    if tema == "Escuro":
        return {
            "Positivo": "#27AE60",
            "Neutro": "#F1C40F",
            "Negativo": "#E74C3C",
            "Elogios": "#27AE60",
            "Sugestões": "#F1C40F",
            "Críticas": "#E74C3C"
        }
    else:
        return {
            "Positivo": "#2ECC71",
            "Neutro": "#F8CAA0",
            "Negativo": "#E74C3C",
            "Elogios": "#2ECC71",
            "Sugestões": "#F8CAA0",
            "Críticas": "#E74C3C"
        }


# Configuração inicial
st.set_page_config(page_title="Amei, nota zero", layout="wide")
st.title("Amei, nota zero")
st.markdown("Automatização de análise de avaliações textuais em negócios online")


# Painel de Acessibilidade Visual
st.sidebar.markdown("### ♿ Acessibilidade Visual")
tema = st.sidebar.selectbox("🎨 Tema visual", ["Claro", "Escuro"])
tamanho_fonte = st.sidebar.selectbox("🔠 Tamanho da fonte", ["Padrão", "Grande", "Extra Grande"])
aplicar_estilos(tema, tamanho_fonte)


# Funções auxiliares
def carregar_arquivo(arquivo):
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
            return None
        st.session_state["df_avaliacoes"] = df
        return df
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
        return None


def exibir_dados(df):
    st.success("✅ Arquivo carregado com sucesso!")
    st.write("Visualização dos dados enviados:")
    st.dataframe(df.head())


def gerar_resumo(df):
    textos = df["Texto"].dropna().astype(str).tolist()
    textos_limpos = [re.sub(r"[^\w\s]", "", t.lower()) for t in textos]
    elogios = ["bom", "ótimo", "excelente", "maravilhoso", "adoro", "recomendo"]
    criticas = ["ruim", "péssimo", "demorado", "caro", "não gostei", "problema"]
    sugestoes = ["poderia", "deveria", "sugiro", "seria melhor", "melhorar"]
    contagem_elogios = sum(any(p in t for p in elogios) for t in textos_limpos)
    contagem_criticas = sum(any(p in t for p in criticas) for t in textos_limpos)
    contagem_sugestoes = sum(any(p in t for p in sugestoes) for t in textos_limpos)
    palavras = " ".join(textos_limpos).split()
    top_palavras = Counter(palavras).most_common(5)
    temas = ", ".join([p[0] for p in top_palavras])
    resumo = f"""
    Foram analisadas {len(df)} avaliações.  
    Identificamos {contagem_elogios} elogios, {contagem_criticas} críticas e {contagem_sugestoes} sugestões.  
    Os temas mais recorrentes incluem: {temas}.  
    Recomenda-se atenção especial aos pontos críticos e valorização dos aspectos positivos percebidos pelos clientes.
    """
    return resumo


# Navegação
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Ir para:", [
    "Início", "Análise de Sentimento", "Tópicos Relevantes",
    "Resumo de Insights", "Visualização de Dados", "Relatório Final"
])


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
    - Relatório final
    """)
    st.caption("Você pode enviar arquivos nos formatos PDF, CSV, Excel, TXT ou JSON.")
    arquivo = st.file_uploader("📁 Envie um arquivo com avaliações", type=["csv", "xlsx", "txt", "json", "pdf"])
    if arquivo:
        df = carregar_arquivo(arquivo)
        if df is not None:
            exibir_dados(df)


# Página: Análise de Sentimento
elif pagina == "Análise de Sentimento":
    st.header("Análise de Sentimento")
    if "df_avaliacoes" in st.session_state:
        df = st.session_state["df_avaliacoes"]
        sentimentos = pd.DataFrame({
            "Sentimento": ["Positivo", "Neutro", "Negativo"],
            "Quantidade": [len(df)//2, len(df)//4, len(df)//4]
        })
    else:
        st.info("⚠️ Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
        sentimentos = pd.DataFrame({
            "Sentimento": ["Positivo", "Neutro", "Negativo"],
            "Quantidade": [42, 18, 25]
        })
    cores = obter_paleta(tema)
    ordem = ["Positivo", "Neutro", "Negativo"]
    chart = alt.Chart(sentimentos).mark_bar().encode(
        x=alt.X("Sentimento", sort=ordem),
        y="Quantidade",
        color=alt.Color("Sentimento", scale=alt.Scale(domain=list(cores.keys()), range=list(cores.values())))
    ).properties(width=600, height=400)
    st.altair_chart(chart, use_container_width=True)


# Página: Tópicos Relevantes
elif pagina == "Tópicos Relevantes":
    st.header("Tópicos Mais Frequentes")
    if "df_avaliacoes" in st.session_state:
        df = st.session_state["df_avaliacoes"]
        palavras = pd.Series(" ".join(df["Texto"]).lower().split())
        top_palavras = palavras.value_counts().head(10)
        st.markdown("Tópicos extraídos das avaliações:")
        for palavra in top_palavras.index:
            st.markdown(f"- {palavra}")
    else:
        st.caption("⚠️ Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
        topicos = ["atendimento", "preço", "qualidade", "tempo de espera", "ambiente", "profissionalismo"]
        for item in topicos:
            st.markdown(f"- {item}")


# Página: Resumo de Insights
elif pagina == "Resumo de Insights":
    st.header("Resumo Inteligente")
    if "df_avaliacoes" in st.session_state:
        df = st.session_state["df_avaliacoes"]
        resumo = gerar_resumo(df)
        st.markdown(f"> {resumo}")
    else:
        st.caption("⚠️ Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
        st.markdown("""
        > “Os clientes elogiam fortemente o atendimento e a qualidade dos serviços, mas há críticas recorrentes sobre o tempo de espera.  
        Recomenda-se otimizar o agendamento para melhorar a experiência geral.”
        """)


# Página: Visualização de Dados
elif pagina == "Visualização de Dados":
    st.header("Painel de Visualização")
    if "df_avaliacoes" in st.session_state:
        df = st.session_state["df_avaliacoes"]
        dados = pd.DataFrame({
            "Categoria": ["Elogios", "Sugestões", "Críticas"],
            "Volume": [len(df)//2, len(df)//6, len(df)//3]
        })
    else:
        st.caption("⚠️ Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
        dados = pd.DataFrame({
            "Categoria": ["Elogios", "Sugestões", "Críticas"],
            "Volume": [60, 10, 30]
        })


    ordem = ["Elogios", "Sugestões", "Críticas"]
    cores = obter_paleta(tema)


    chart = alt.Chart(dados).mark_bar().encode(
        x=alt.X("Categoria", sort=ordem),
        y="Volume",
        color=alt.Color("Categoria", scale=alt.Scale(domain=list(cores.keys()), range=list(cores.values())))
    ).properties(width=600, height=400)


    st.altair_chart(chart, use_container_width=True)


# Página: Relatório Final
elif pagina == "Relatório Final":
    st.header("📄 Relatório Final de Avaliações")
    if "df_avaliacoes" in st.session_state:
        df = st.session_state["df_avaliacoes"]
        resumo = gerar_resumo(df)


        st.markdown("#### 1. Visão Geral")
        st.markdown(f"- Total de avaliações analisadas: **{len(df)}**")
        st.markdown("- Formato original do arquivo: **Texto Livre**")
        st.markdown("- Fonte: Arquivo enviado pelo usuário")


        st.markdown("#### 2. Distribuição de Sentimentos (simulada)")
        positivos = len(df) // 2
        neutros = len(df) // 4
        negativos = len(df) // 4
        st.markdown(f"- Positivas: **{positivos}**")
        st.markdown(f"- Neutras: **{neutros}**")
        st.markdown(f"- Negativas: **{negativos}**")


        st.markdown("#### 3. Tópicos Mais Frequentes")
        palavras = pd.Series(" ".join(df["Texto"]).lower().split())
        top_palavras = palavras.value_counts().head(10)
        for i, palavra in enumerate(top_palavras.index, 1):
            st.markdown(f"{i}. {palavra}")


        st.markdown("#### 4. Resumo Inteligente")
        st.markdown(f"> {resumo}")


        st.markdown("#### 5. Recomendação Final")
        st.markdown("""
        - Priorizar melhorias nos pontos críticos identificados  
        - Monitorar avaliações futuras para medir impacto das ações  
        - Repetir análise periodicamente para manter o alinhamento com a experiência do cliente
        """)


        st.markdown("---")
        st.caption("Este relatório foi gerado automaticamente com base nas avaliações enviadas.")
        st.info("💡 Dica: Para salvar este relatório, use a opção 'Imprimir como PDF' do seu navegador.")
    else:
        st.warning("⚠️ Nenhum arquivo foi carregado ainda. Por favor, envie um arquivo na aba 'Início' para gerar o relatório.")


# Rodapé
st.markdown("---")
st.caption("Este aplicativo foi desenvolvido com foco em acessibilidade visual, seguindo os princípios do WCAG 2.1.")
st.caption("Projeto Integrador - Univesp | Grupo DRP01-PJI240-SALA005GRUPO-006")
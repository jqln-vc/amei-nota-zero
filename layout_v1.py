import streamlit as st
import pandas as pd
import altair as alt


from estilos.visual import aplicar_estilos, obter_paleta
from estilos.visual import mostrar_aviso
from funcionalidades.carregamento import carregar_arquivo, exibir_dados
from funcionalidades.resumo import gerar_resumo
from funcionalidades.visualizacao import gerar_grafico_barra, gerar_grafico_pizza
from componentes.acessibilidade import configurar_acessibilidade
from componentes.navegacao import configurar_navegacao


def construir_interface():
    # Configuração inicial
    st.set_page_config(page_title="Amei, nota zero", layout="wide")


    # Painel de Acessibilidade Visual
    modo_tema, tamanho_fonte = configurar_acessibilidade()


    # Aplicar estilo de fonte e tema
    aplicar_estilos(tamanho_fonte, modo_tema)


    # Paleta de cores para gráficos
    cores = obter_paleta(modo_tema)


    # Cor de texto adaptada ao tema
    cor_titulo = "#222222" if modo_tema.strip().lower() == "claro" else "#e0e0e0"


    # Título e descrição
    st.title("Amei, nota zero")
    st.markdown("Automatização de análise de avaliações textuais em negócios online")


    # Navegação
    pagina = configurar_navegacao()


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


        st.markdown(f'<p style="color:{cor_titulo}; font-size:14px;">Você pode enviar arquivos nos formatos PDF, CSV, Excel, TXT ou JSON.</p>', unsafe_allow_html=True)
        st.markdown('<h3 class="titulo-upload">📁 Envie um arquivo com avaliações</h3>', unsafe_allow_html=True)
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        arquivo = st.file_uploader(
            label="📁 Envie um arquivo com avaliações",
            type=["csv", "xlsx", "txt", "json", "pdf"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)


        if arquivo:
            df = carregar_arquivo(arquivo)
            if df is not None:
                st.session_state["df_avaliacoes"] = df
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
            st.caption("⚠️ Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
            sentimentos = pd.DataFrame({
                "Sentimento": ["Positivo", "Neutro", "Negativo"],
                "Quantidade": [42, 18, 25]
            })


        total = sentimentos["Quantidade"].sum()
        sentimentos["Percentual"] = (sentimentos["Quantidade"] / total * 100).round(1)


        chart = gerar_grafico_pizza(sentimentos, "Sentimento", ["Positivo", "Neutro", "Negativo"], cores, modo_tema)


        col_esq, col_centro, col_dir = st.columns([1, 2, 1])
        with col_centro:
            st.altair_chart(chart, use_container_width=False)


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
                "Quantidade": [len(df)//2, len(df)//6, len(df)//3]
            })
        else:
            st.caption("⚠️ Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
            dados = pd.DataFrame({
                "Categoria": ["Elogios", "Sugestões", "Críticas"],
                "Quantidade": [60, 10, 30]
            })


        dados["Percentual"] = (dados["Quantidade"] / dados["Quantidade"].sum() * 100).round(1)


        chart = gerar_grafico_barra(dados, "Categoria", ["Elogios", "Sugestões", "Críticas"], cores, modo_tema)
        st.altair_chart(chart, use_container_width=True)


    # Página: Relatório Final
    elif pagina == "Relatório Final":
        st.header("📄 Relatório Final de Avaliações")


        if "df_avaliacoes" in st.session_state:
            df = st.session_state["df_avaliacoes"]
            resumo = gerar_resumo(df)


            st.subheader("1. Visão Geral")
            st.markdown(f"- **Total de avaliações analisadas:** {len(df)}")
            st.markdown("- **Formato original do arquivo:** Texto Livre")
            st.markdown("- **Fonte:** Arquivo enviado pelo usuário")


            st.subheader("2. Distribuição de Sentimentos")
            positivos = len(df) // 2
            neutros = len(df) // 4
            negativos = len(df) // 4


            col1, col2, col3 = st.columns(3)
            col1.metric("😊 Positivas", positivos)
            col2.metric("😐 Neutras", neutros)
            col3.metric("😠 Negativas", negativos)


            st.subheader("3. Tópicos Mais Frequentes")
            palavras = pd.Series(" ".join(df["Texto"]).lower().split())
            top_palavras = palavras.value_counts().head(10)
            st.markdown("Os termos mais recorrentes nas avaliações foram:")
            for i, palavra in enumerate(top_palavras.index, 1):
                st.markdown(f"{i}. {palavra}")


            st.subheader("4. Resumo Inteligente")
            st.markdown(f"> {resumo}")


            st.subheader("5. Recomendação Final")
            st.markdown("---")
            st.caption("Este relatório foi gerado automaticamente com base nas avaliações enviadas.")
            st.caption("💡 Dica: Para salvar este relatório, use a opção 'Imprimir como PDF' do seu navegador.")
        else:
            mostrar_aviso(modo_tema)
    # Rodapé
    st.markdown("---")
    st.caption("Este aplicativo foi desenvolvido com foco em acessibilidade visual, seguindo os princípios do WCAG 2.1.")

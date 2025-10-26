import streamlit as st
import pandas as pd
import altair as alt

from estilos.visual import aplicar_estilos, obter_paleta, mostrar_aviso, cor_texto_tema
from funcionalidades.carregamento import carregar_arquivo, exibir_dados
from funcionalidades.resumo import gerar_resumo
from funcionalidades.visualizacao import gerar_grafico_barra
from componentes.acessibilidade import configurar_acessibilidade
from componentes.navegacao import configurar_navegacao

def mostrar_erro_personalizado(modo_tema: str, mensagem: str):
    cor = cor_texto_tema(modo_tema)
    html = f"""
    <div style='color:{cor}; font-size:120%; border-left: 6px solid #FF6F61; padding: 0.5em 0.75em; margin: 0.5em 0; background-color: transparent; box-shadow: none;'>
        <strong>AVISO:</strong> {mensagem}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def construir_interface():
    st.set_page_config(page_title="Amei, nota zero", layout="wide")

    modo_tema, tamanho_fonte = configurar_acessibilidade()
    aplicar_estilos(tamanho_fonte, modo_tema)
    cor = cor_texto_tema(modo_tema)

    st.title("Amei, nota zero")
    st.markdown(f"<p style='color:{cor}; font-size:120%;'>Automatização de análise de avaliações textuais em negócios online</p>", unsafe_allow_html=True)

    pagina = configurar_navegacao()
    categorias = ["Elogios", "Sugestões", "Críticas"]
    cores = [obter_paleta(modo_tema)[c] for c in categorias]

    if pagina == "Início":
        st.header("Que bom ter você por aqui!")
        st.markdown(f"""
            <p style='color:{cor}; font-size:120%;'>
            Este aplicativo foi criado para ajudar microempreendedores a entender melhor o que seus clientes estão dizendo.<br><br>
            Nós vamos transformar suas avaliações textuais em <strong>insights acionáveis</strong>.
            </p>
            <ul style='color:{cor}; font-size:120%;'>
                <li>Extração de tópicos</li>
                <li>Resumo inteligente</li>
                <li>Visualização de dados</li>
                <li>Relatório final</li>
            </ul>
            <p style='color:{cor}; font-size:120%;'>Você pode enviar arquivos nos formatos CSV, Excel, TXT ou JSON.</p>
        """, unsafe_allow_html=True)

        st.markdown('<h3 class="titulo-upload">📁 Envie um arquivo com avaliações</h3>', unsafe_allow_html=True)
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        arquivo = st.file_uploader("📁 Envie um arquivo com avaliações", type=["csv", "xlsx", "txt", "json"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        if arquivo:
            df = carregar_arquivo(arquivo)
            if df is not None:
                exibir_dados(df)

    elif pagina == "Análise de Avaliações":
        st.header("📊 Análise de Avaliações")
        st.subheader("Visualização de Dados")

        if "df_avaliacoes" in st.session_state:
            df = st.session_state["df_avaliacoes"]
            dados = pd.DataFrame({
                "Categoria": categorias,
                "Quantidade": [len(df)//2, len(df)//6, len(df)//3]
            })
        else:
            mostrar_erro_personalizado(modo_tema, "Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
            dados = pd.DataFrame({
                "Categoria": categorias,
                "Quantidade": [60, 10, 30]
            })

        dados["Percentual"] = (dados["Quantidade"] / dados["Quantidade"].sum() * 100).round(1)
        st.altair_chart(gerar_grafico_barra(dados, "Categoria", categorias, cores, modo_tema), use_container_width=True)

        st.subheader("Tópicos Mais Frequentes")
        if "df_avaliacoes" in st.session_state:
            coluna = next((c for c in df.columns if c.lower() in ["texto", "comentário", "mensagem"]), None)
            if coluna:
                palavras = pd.Series(" ".join(df[coluna].astype(str)).lower().split())
                top = palavras.value_counts().head(10)
                st.markdown(f"<p style='color:{cor}; font-size:120%;'>Tópicos extraídos das avaliações:</p>", unsafe_allow_html=True)
                for p in top.index:
                    st.markdown(f"<p style='color:{cor}; font-size:120%;'>- {p}</p>", unsafe_allow_html=True)
            else:
                mostrar_erro_personalizado(modo_tema, "Nenhuma coluna de texto foi encontrada no arquivo enviado.")
        else:
            for item in ["atendimento", "preço", "qualidade", "tempo de espera", "ambiente", "profissionalismo"]:
                st.markdown(f"<p style='color:{cor}; font-size:120%;'>- {item}</p>", unsafe_allow_html=True)

        st.subheader("Resumo Inteligente")
        if "df_avaliacoes" in st.session_state:
            resumo = gerar_resumo(df)
            st.markdown(f"<p style='color:{cor}; font-size:120%;'>{resumo}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <p style='color:{cor}; font-size:120%;'>
                “Os clientes elogiam fortemente o atendimento e a qualidade dos serviços, mas há críticas recorrentes sobre o tempo de espera.<br>
                Recomenda-se otimizar o agendamento para melhorar a experiência geral.”
                </p>
            """, unsafe_allow_html=True)

    elif pagina == "Relatório Final":
        st.header("📄 Relatório Final de Avaliações")

        if "df_avaliacoes" in st.session_state:
            df = st.session_state["df_avaliacoes"]
            resumo = gerar_resumo(df)

            st.subheader("1. Visão Geral")
            st.markdown(f"<p style='color:{cor}; font-size:120%;'>- <strong>Total de avaliações analisadas:</strong> {len(df)}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:{cor}; font-size:120%;'>- <strong>Formato original do arquivo:</strong> Texto Livre</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:{cor}; font-size:120%;'>- <strong>Fonte:</strong> Arquivo enviado pelo usuário</p>", unsafe_allow_html=True)

            st.subheader("2. Tópicos Mais Frequentes")
            coluna = next((c for c in df.columns if c.lower() in ["texto", "comentário", "mensagem"]), None)
            if coluna:
                palavras = pd.Series(" ".join(df[coluna].astype(str)).lower().split())
                top = palavras.value_counts().head(10)
                st.markdown(f"<p style='color:{cor}; font-size:120%;'>Os termos mais recorrentes nas avaliações foram:</p>", unsafe_allow_html=True)
                for i, p in enumerate(top.index, 1):
                    st.markdown(f"<p style='color:{cor}; font-size:120%;'>{i}. {p}</p>", unsafe_allow_html=True)
            else:
                mostrar_erro_personalizado(modo_tema, "Nenhuma coluna de texto foi encontrada no arquivo enviado.")

            st.subheader("3. Resumo Inteligente")
            st.markdown(f"<p style='color:{cor}; font-size:120%;'>{resumo}</p>", unsafe_allow_html=True)

            st.subheader("4. Recomendação Final")
            st.markdown("---")
            st.caption(f"<span style='color:{cor}; font-size:120%;'>Este relatório foi gerado automaticamente com base nas avaliações enviadas.</span>", unsafe_allow_html=True)
        else:
            mostrar_aviso(modo_tema)

        st.markdown("---")
        st.caption(f"<span style='color:{cor}; font-size:120%;'>Este aplicativo foi desenvolvido com foco em acessibilidade visual, seguindo os princípios do WCAG 2.1.</span>", unsafe_allow_html=True)

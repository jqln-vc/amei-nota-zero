import streamlit as st
import pandas as pd
from estilos.visual import aplicar_estilos, obter_paleta, cor_texto_tema
from funcionalidades.carregamento import carregar_arquivo, exibir_dados
from funcionalidades.resumo import gerar_resumo
from funcionalidades.visualizacao import gerar_grafico_barra
from componentes.acessibilidade import configurar_acessibilidade
from componentes.navegacao import configurar_navegacao

def mostrar_erro_personalizado(modo_tema, mensagem):
    cor = cor_texto_tema(modo_tema)
    html = f"""
    <div style='color:{cor}; font-size:120%; border-left: 6px solid #FF6F61; padding: 0.5em 0.75em; margin: 0.5em 0;'>
        <strong>AVISO:</strong> {mensagem}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def construir_interface():
    # 1. Configuração de página
    st.set_page_config(page_title="Amei, nota zero", layout="wide")

    # 2. Sidebar: Navegação e Acessibilidade
    pagina = configurar_navegacao()
    modo_tema, tamanho_fonte = configurar_acessibilidade()

    # 3. Aplicação de estilos CSS globais 
    aplicar_estilos(tamanho_fonte, modo_tema)
    
    cor = cor_texto_tema(modo_tema)
    categorias = ["Elogios", "Sugestões", "Críticas"]
    paleta = obter_paleta(modo_tema)
    cores = [paleta[c] for c in categorias]

    if pagina == "Início":
        st.title("Amei, nota zero")
        st.subheader("Automatização de análise de avaliações textuais em negócios online")
        
        st.markdown(f"**Transforme o feedback dos seus clientes em decisões inteligentes de forma automática.**")
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Análise Inteligente**\n\nDescubra os tópicos mais comentados.")
        with col2:
            st.warning("**Visão Clara**\n\nDashboards dinâmicos para melhoria contínua.")
        with col3:
            st.success("**Ação Rápida**\n\nReceba resumos gerados por IA.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Comece por aqui")
        
        arquivo = st.file_uploader(label="Arraste ou selecione seu arquivo de avaliações", type=["csv", "xlsx", "txt", "json"])
        
        if arquivo:
            df = carregar_arquivo(arquivo)
            if df is not None:
                st.session_state["df_avaliacoes"] = df
                exibir_dados(df)

    elif pagina == "Análise de Avaliações":
        st.header("📊 Análise de Avaliações")
        
        if "df_avaliacoes" in st.session_state and st.session_state["df_avaliacoes"] is not None:
            df = st.session_state["df_avaliacoes"]
            total_avaliacoes = len(df)
            
            # Simulando distribuição 
            qtd_elogios = total_avaliacoes // 2
            qtd_criticas = total_avaliacoes // 3
            qtd_sugestoes = total_avaliacoes - (qtd_elogios + qtd_criticas)
            
            dados_grafico = pd.DataFrame({
                "Categoria": categorias,
                "Quantidade": [qtd_elogios, qtd_sugestoes, qtd_criticas]
            })

            # Métricas
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total", total_avaliacoes)
            c2.metric("Elogios", qtd_elogios)
            c3.metric("Sugestões", qtd_sugestoes)
            c4.metric("Críticas", qtd_criticas)

            st.markdown("---")
            col_grafico, _, col_topicos = st.columns([6, 0.5, 3.5])
            
            with col_grafico:
                st.subheader("Visualização de Dados")
                # Passando o modo_tema para o gráfico seguir a cor do texto
                fig = gerar_grafico_barra(dados_grafico, "Categoria", categorias, cores, modo_tema)
                st.altair_chart(fig, use_container_width=True)

            with col_topicos:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.subheader("Top 5 Tópicos")
                st.write(f"✓ **Atendimento**")
                st.write(f"✓ **Qualidade**")
                st.write(f"✓ **Preço**")

            st.markdown("---")
            st.subheader("🤖 Resumo Inteligente")
            with st.container(border=True):
                resumo = gerar_resumo(df)
                st.write(resumo)
        else:
            mostrar_erro_personalizado(modo_tema, "Nenhum arquivo enviado. Por favor, faça o upload na aba 'Início'.")
import streamlit as st
from funcionalidades.carregamento import carregar_arquivo
from funcionalidades.visualizacao import gerar_grafico_altair
from funcionalidades.resumo import exibir_resumo
from estilos.visual import aplicar_estilos, mostrar_aviso, cor_texto_tema

def construir_interface():
    tamanho_fonte = st.session_state.get("tamanho_fonte", "Padrão")
    modo_tema = st.session_state.get("modo_tema", "Claro")
    cor_txt = cor_texto_tema(modo_tema)
    
    # Define a cor da borda com base no tema (cinza claro para tema claro, cinza escuro para tema escuro)
    cor_borda = "#dcdcdc" if modo_tema.strip().lower() == "claro" else "#444444"

    aplicar_estilos(tamanho_fonte, modo_tema)

    with st.sidebar:
        st.markdown("### 🗺️ Navegação")
        
        if "pagina_ativa" not in st.session_state:
            st.session_state["pagina_ativa"] = "Início"

        tipo_inicio = "primary" if st.session_state["pagina_ativa"] == "Início" else "secondary"
        if st.button("Início", key="btn_inicio", type=tipo_inicio, use_container_width=True):
            st.session_state["pagina_ativa"] = "Início"
            st.rerun()

        tipo_analise = "primary" if st.session_state["pagina_ativa"] == "Análise de Avaliações" else "secondary"
        if st.button("Análise de Avaliações", key="btn_analise", type=tipo_analise, use_container_width=True):
            st.session_state["pagina_ativa"] = "Análise de Avaliações"
            st.rerun()

        st.markdown("---")
        from componentes.acessibilidade import construir_acessibilidade
        construir_acessibilidade()

    pagina = st.session_state["pagina_ativa"]

    if pagina == "Início":
        # Textos do cabeçalho ajustados para reproduzir exatamente a referência visual
        st.markdown(f"<h1 style='color:{cor_txt}; font-size: 2.5rem; margin-bottom: 0.2rem; padding-bottom: 0;'>Amei, nota zero</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{cor_txt}; font-size: 1.05rem; margin-top: 0; margin-bottom: 2rem;'>Automatização de análise de avaliações textuais em negócios online</p>", unsafe_allow_html=True)

        st.markdown(f"<h2 style='color:{cor_txt}; margin-bottom: 0.5rem;'>Que bom ter você por aqui!</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{cor_txt}; font-size: 1.05rem; margin-bottom: 1.5rem;'>Transforme o feedback dos seus clientes em <strong>decisões inteligentes</strong> para o seu negócio de forma automática.</p>", unsafe_allow_html=True)

        # Linha divisória sutil idêntica à foto
        st.markdown(f"<hr style='margin-top: 20px; margin-bottom: 30px; border: 0; border-top: 1px solid {cor_borda}; opacity: 0.6;'>", unsafe_allow_html=True)

        # Cards Informativos no formato de caixas com borda (idêntico à referência)
        col_c1, col_c2, col_c3 = st.columns(3)
        
        estilo_card = f"border: 1px solid {cor_borda}; border-radius: 6px; padding: 20px; height: 100%; min-height: 140px; display: flex; flex-direction: column;"
        estilo_titulo_card = f"font-weight: 600; font-size: 0.95rem; margin-bottom: 15px; color: {cor_txt};"
        estilo_texto_card = f"font-size: 0.9rem; color: {cor_txt}; line-height: 1.6; opacity: 0.9;"

        with col_c1:
            st.markdown(f"""
            <div style="{estilo_card}">
                <div style="{estilo_titulo_card}">🧠 Análise Inteligente</div>
                <div style="{estilo_texto_card}">Descubra os <strong>tópicos</strong> mais comentados e o sentimento por trás de cada avaliação.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_c2:
            st.markdown(f"""
            <div style="{estilo_card}">
                <div style="{estilo_titulo_card}">📊 Visão Clara</div>
                <div style="{estilo_texto_card}">Dashboards dinâmicos para você entender rapidamente onde acertou e onde melhorar.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_c3:
            st.markdown(f"""
            <div style="{estilo_card}">
                <div style="{estilo_titulo_card}">📄 Ação Rápida</div>
                <div style="{estilo_texto_card}">Receba resumos gerados por IA e recomendações práticas no seu relatório final.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Título da seção de upload idêntico à imagem (com ícone de link)
        st.markdown(f"<h3 style='color:{cor_txt}; display: flex; align-items: center; gap: 8px;'>Comece por aqui 👇 <span style='font-size: 1rem; opacity: 0.5;'>🔗</span></h3>", unsafe_allow_html=True)
        
        arquivo_carregado = carregar_arquivo()
        if arquivo_carregado is not None:
            st.session_state["dados_carregados"] = arquivo_carregado
            st.success("Arquivo carregado com sucesso!")

    elif pagina == "Análise de Avaliações":
        st.title("Análise de Avaliações")

        if "dados_carregados" in st.session_state:
            df = st.session_state["dados_carregados"]
        else:
            mostrar_aviso("AVISO: Nenhum arquivo enviado. Exibindo dados de exemplo.", modo_tema)
            import pandas as pd
            df = pd.DataFrame({"Sentimento": ["Elogios"]*60 + ["Sugestões"]*10 + ["Criticas"]*30})

        # Alinhamento da aba de análise consolidado nas requisições anteriores
        m1, m2, m3, m4 = st.columns([1.3, 1, 1, 1])
        
        estilo_titulo = f"color:{cor_txt}; opacity:0.9; font-size:1.15rem; font-weight:600; display:block; margin-bottom:12px; white-space:nowrap;"
        estilo_numero = f"color:{cor_txt}; font-size:1.8rem; font-weight:bold; margin:0; display:block;"
        
        with m1:
            st.markdown(f"<div><span style='{estilo_titulo}'>Total de Avaliações</span><span style='{estilo_numero}'>{len(df)}</span></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div><span style='{estilo_titulo}'>🟢 Elogios</span><span style='{estilo_numero}'>60</span></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div><span style='{estilo_titulo}'>🟡 Sugestões</span><span style='{estilo_numero}'>10</span></div>", unsafe_allow_html=True)
        with m4:
            st.markdown(f"<div><span style='{estilo_titulo}'>🔴 Críticas</span><span style='{estilo_numero}'>30</span></div>", unsafe_allow_html=True)

        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.subheader("Visualização de Dados")

        col_graph, col_topics = st.columns([2.2, 1], gap="large")
        with col_graph:
            gerar_grafico_altair(df, modo_tema)
        with col_topics:
            st.markdown("### Top 5 Tópicos")
            st.markdown("✔️ Atendimento\n\n✔️ Preço\n\n✔️ Qualidade\n\n✔️ Espera\n\n✔️ Ambiente")

        st.markdown("---")
        exibir_resumo(df, modo_tema)
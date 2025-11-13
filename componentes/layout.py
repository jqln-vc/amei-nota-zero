import streamlit as st
import pandas as pd
import altair as alt

from estilos.visual import aplicar_estilos, obter_paleta, cor_texto_tema
from funcionalidades.carregamento import carregar_arquivo, exibir_dados, gerar_relatorio
from funcionalidades.user_crud import conectar_banco, salvar_avaliacoes, carregar_avaliacoes 
from funcionalidades.visualizacao import gerar_grafico_barra
from componentes.acessibilidade import configurar_acessibilidade
from componentes.navegacao import configurar_navegacao
import funcionalidades.nlp as nlp

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
    st.session_state["modo_tema"] = modo_tema
    aplicar_estilos(tamanho_fonte, modo_tema)
    cor = cor_texto_tema(modo_tema)

    st.title("Amei, nota zero")
    st.markdown(f"<p style='color:{cor}; font-size:120%;'>Automatização de análise de avaliações textuais em negócios online</p>", unsafe_allow_html=True)

    pagina = configurar_navegacao()
    categorias = ["positive", "neutral", "negative"]
    cores = [obter_paleta(modo_tema)[c] for c in categorias]
    
    # Osbter o objeto de conexão cacheado
    conn = conectar_banco()

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
            df_raw = carregar_arquivo(arquivo)
            df, all_reviews = nlp.extrair_sentimento(df_raw[1:])
            if not df.empty and all_reviews is not None:
                extracted_info = nlp.processar_reviews(all_reviews)
                st.session_state["resumo"] = extracted_info["summary"]
                st.session_state["topicos"] = extracted_info["key_topics"]
                st.session_state["recomendacao"] = extracted_info["advice"]
                st.session_state["empresa"] = df["name"].iloc[0]
                st.session_state["df_avaliacoes"] = df

            if st.button("💾 Salvar no banco de dados",
                        type="tertiary"):
                salvar_avaliacoes(df, conn)
                exibir_dados(carregar_avaliacoes(conn))
            else:
                exibir_dados(df)
            
                
            
                
                

    elif pagina == "Análise de Avaliações":
        empresa = st.session_state.get("empresa", "Sua Empresa")
        resumo = st.session_state.get("resumo", "")
        topicos = st.session_state.get("topicos", [])
        recomendacao = st.session_state.get("recomendacao", "")

        st.header(f"📊 Análise de Avaliações de {empresa}")
        
        st.subheader("Gráfico de Análise de Sentimento")
        if "df_avaliacoes" in st.session_state:
            df_sent = st.session_state["df_avaliacoes"]["sent_tag"].value_counts().reset_index()
            dados = pd.DataFrame({
                    "Categoria": df_sent.iloc[:, 0].tolist(),
                    "Quantidade": df_sent.iloc[:, 1].tolist()
                })
        else:
            mostrar_erro_personalizado(modo_tema, "Nenhum arquivo ainda foi enviado. Você está vendo um exemplo com dados fictícios.")
            
        dados["Percentual"] = (dados["Quantidade"] / dados["Quantidade"].sum() * 100).round(1)
        grafico_sent = gerar_grafico_barra(dados, "Categoria", categorias, cores, modo_tema)
        st.altair_chart(grafico_sent, use_container_width=True)

        st.subheader("Tópicos Mais Frequentes")
        if "df_avaliacoes" in st.session_state:
                for item in topicos:
                    st.markdown(f"<p style='color:{cor}; font-size:120%;'>- {item}</p>", unsafe_allow_html=True)

        st.subheader("Resumo Inteligente")
        if "df_avaliacoes" in st.session_state:
            st.markdown(f"<p style='color:{cor}; font-size:120%;'>{resumo}</p>", unsafe_allow_html=True)
        
        st.subheader("Recomendação")
        if "df_avaliacoes" in st.session_state:
            st.markdown(f"<p style='color:{cor}; font-size:120%;'>{recomendacao}</p>", unsafe_allow_html=True)

        pdf_bytes = gerar_relatorio(empresa, grafico_sent, topicos, resumo, recomendacao)

        
        st.download_button(
            label="📥 Baixar Relatório em PDF",
            data=bytes(pdf_bytes),
            file_name=f"relatorio_analise_avaliacoes_{empresa.replace(' ', '_').lower()}.pdf",
            mime="application/pdf",
            type="tertiary",
            use_container_width=True
        )

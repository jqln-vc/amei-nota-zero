import altair as alt
import pandas as pd
from estilos.visual import cor_texto_tema

def gerar_grafico_barra(dados, coluna_x, categorias, cores, modo_tema):
    """
    Gera um gráfico de barras estilizado que adapta as cores do texto
    conforme o tema (Claro/Escuro) selecionado.
    """
    # Obtém a cor correta para as letras (Preto ou Branco)
    cor_texto = cor_texto_tema(modo_tema)
    
    # Garante que o cálculo de percentual exista para o Tooltip
    if "Percentual" not in dados.columns:
        total = dados["Quantidade"].sum()
        dados["Percentual"] = (dados["Quantidade"] / total * 100) if total > 0 else 0

    # Configuração das Barras
    barras = alt.Chart(dados).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5
    ).encode(
        x=alt.X(f"{coluna_x}:N",
                sort=categorias,
                axis=alt.Axis(
                    title=None, 
                    labelColor=cor_texto, 
                    grid=False, 
                    labelAngle=0,
                    labelFontSize=12
                )),
        y=alt.Y("Quantidade:Q",
                axis=alt.Axis(
                    title="Quantidade", 
                    labelColor=cor_texto, 
                    titleColor=cor_texto,
                    grid=False
                )),
        color=alt.Color("Categoria:N",
                        scale=alt.Scale(domain=categorias, range=cores),
                        legend=None),
        tooltip=[
            alt.Tooltip("Categoria:N", title="Categoria"),
            alt.Tooltip("Quantidade:Q", title="Total"),
            alt.Tooltip("Percentual:Q", title="Proporção (%)", format=".1f")
        ]
    )

    # Rótulos de texto (números acima das barras)
    rotulos = alt.Chart(dados).mark_text(
        align="center",
        baseline="bottom",
        dy=-5,
        fontSize=14,
        fontWeight="bold"
    ).encode(
        x=alt.X(f"{coluna_x}:N", sort=categorias),
        y=alt.Y("Quantidade:Q"),
        text=alt.Text("Quantidade:Q"),
        color=alt.value(cor_texto)  # Força o número a seguir o tema
    )

    # Composição final e configurações de visualização
    chart = (barras + rotulos).properties(
        height=350,
        background='transparent'
    ).configure_view(
        stroke=None,
        fill='transparent'
    ).configure_axis(
        domain=False,
        ticks=False
    )
    
    return chart
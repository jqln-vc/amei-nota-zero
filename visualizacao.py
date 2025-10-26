import altair as alt
import pandas as pd

def gerar_grafico_barra(dados, campo_x, categorias, cores, modo_tema):
    # Cor adaptada ao tema
    cor_texto = "#222222" if modo_tema.strip().lower() == "claro" else "#e0e0e0"

    # Gráfico de barras
    barras = alt.Chart(dados).mark_bar().encode(
        x=alt.X(campo_x,
                axis=alt.Axis(labelAngle=0,
                              labelFontSize=20,     # legenda inferior ampliada
                              titleFontSize=20,
                              labelColor=cor_texto,
                              titleColor=cor_texto)),
        y=alt.Y("Quantidade:Q",
                axis=alt.Axis(labelFontSize=26,
                              titleFontSize=26,
                              labelColor=cor_texto,
                              titleColor=cor_texto)),
        color=alt.Color(campo_x,
                        scale=alt.Scale(domain=categorias, range=cores),
                        legend=alt.Legend(title="Categoria",
                                          labelFontSize=18,
                                          titleFontSize=18,
                                          labelColor=cor_texto,
                                          titleColor=cor_texto)),
        tooltip=["Categoria", "Quantidade", "Percentual"]
    )

    # Texto percentual acima da barra
    texto_percentual = alt.Chart(dados).mark_text(
        align="center",
        baseline="bottom",
        dy=-5,
        fontWeight="bold",
        fontSize=19.5,
        color=cor_texto
    ).encode(
        x=campo_x,
        y=alt.Y("Quantidade:Q"),
        text=alt.Text("Percentual", format=".1f")
    )

    # Texto absoluto acima do percentual
    texto_absoluto = alt.Chart(dados).mark_text(
        align="center",
        baseline="bottom",
        dy=-25,
        fontWeight="bold",
        fontSize=19.5,
        color=cor_texto
    ).encode(
        x=campo_x,
        y=alt.Y("Quantidade:Q"),
        text=alt.Text("Quantidade", format=".0f")
    )

    # Combina os elementos
    chart = (barras + texto_percentual + texto_absoluto).properties(
        width=600,
        height=400,
        background="transparent"
    ).configure_axis(
        grid=False  # remove todas as linhas de grade
    ).configure_view(
        stroke=None  # remove borda do gráfico
    )

    return chart

import altair as alt
import pandas as pd


def gerar_grafico_barra(df: pd.DataFrame, coluna_categoria: str, categorias: list, cores: dict, modo_tema: str) -> alt.Chart:
    paleta = [cores.get(c, "#999999") for c in categorias]
    cor_texto_legenda = "#222" if modo_tema.strip().lower() == "claro" else "#e0e0e0"


    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(coluna_categoria, sort=categorias),
        y=alt.Y("Quantidade:Q"),
        color=alt.Color(coluna_categoria, scale=alt.Scale(domain=categorias, range=paleta))
    ).properties(
        width=600,
        height=400,
        background="transparent"
    ).configure_legend(
        labelColor=cor_texto_legenda,
        titleColor=cor_texto_legenda
    ).configure_axisX(
        grid=False,
        labelColor=cor_texto_legenda,
        titleColor=cor_texto_legenda
    ).configure_axisY(
        grid=False,
        labelColor=cor_texto_legenda,
        titleColor=cor_texto_legenda
    ).configure_view(
        stroke=None
    )


    return chart


def gerar_grafico_pizza(df: pd.DataFrame, coluna_categoria: str, categorias: list, cores: dict, modo_tema: str) -> alt.Chart:
    paleta = [cores.get(c, "#999999") for c in categorias]
    cor_texto_legenda = "#222" if modo_tema.strip().lower() == "claro" else "#e0e0e0"


    total = df["Quantidade"].sum()
    df["Percentual"] = (df["Quantidade"] / total * 100).round(1)


    chart = alt.Chart(df).mark_arc().encode(
        theta=alt.Theta("Quantidade:Q"),
        color=alt.Color(coluna_categoria, scale=alt.Scale(domain=categorias, range=paleta))
    ).properties(
        width=400,
        height=400,
        background="transparent"
    ).configure_legend(
        labelColor=cor_texto_legenda,
        titleColor=cor_texto_legenda
    ).configure_view(
        stroke=None
    )


    return chart

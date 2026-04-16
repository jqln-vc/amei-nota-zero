import streamlit as st
import altair as alt

def gerar_grafico_altair(df, modo_tema):
    is_claro = modo_tema.strip().lower() == "claro"
    cor_texto = "#222222" if is_claro else "#FFFFFF"
    
    source = [
        {"Categoria": "Elogios", "Quantidade": 60, "Cor": "#009E73"},
        {"Categoria": "Sugestões", "Quantidade": 10, "Cor": "#E69F00"},
        {"Categoria": "Críticas", "Quantidade": 30, "Cor": "#D55E00"}
    ]
    
    data = alt.Data(values=source)

    # SOLUÇÃO DO HOVER: Adicionado o parâmetro 'tooltip' forçando apenas Categoria e Quantidade
    bars = alt.Chart(data).mark_bar().encode(
        x=alt.X('Categoria:N', title=None, sort=None, axis=alt.Axis(labels=False, ticks=False, domain=False)),
        y=alt.Y('Quantidade:Q', title=None, axis=alt.Axis(labelColor=cor_texto, grid=False, ticks=False, domain=False)),
        color=alt.Color('Cor:N', scale=None),
        tooltip=['Categoria:N', 'Quantidade:Q'] 
    )

    text = bars.mark_text(
        align='center', baseline='bottom', dy=-5, fontWeight='bold', fontSize=14
    ).encode(
        text='Quantidade:Q',
        color=alt.value(cor_texto),
        tooltip=['Categoria:N', 'Quantidade:Q']
    )

    chart = (bars + text).properties(height=350).configure(
        background='transparent' 
    ).configure_view(strokeWidth=0)

    st.altair_chart(chart, use_container_width=True, theme=None)
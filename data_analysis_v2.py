import pandas as pd


def gerar_resumo(df: pd.DataFrame) -> str:
    # Simulação de resumo baseado em conteúdo textual
    if "Texto" not in df.columns:
        return "⚠️ Coluna 'Texto' não encontrada no arquivo."


    textos = " ".join(df["Texto"].dropna().astype(str)).lower()


    if "atendimento" in textos and "tempo" in textos:
        return (
            "Os clientes elogiam fortemente o atendimento e a qualidade dos serviços, "
            "mas há críticas recorrentes sobre o tempo de espera. "
            "Recomenda-se otimizar o agendamento para melhorar a experiência geral."
        )
    elif "preço" in textos:
        return (
            "Há menções frequentes ao preço, com destaque para a percepção de custo-benefício. "
            "Promoções e transparência podem reforçar esse ponto positivo."
        )
    else:
        return (
            "As avaliações indicam aspectos variados da experiência do cliente. "
            "Recomenda-se uma análise mais aprofundada para identificar padrões específicos."
        )

import re
from collections import Counter


def gerar_resumo(df):
    textos = df["Texto"].dropna().astype(str).tolist()
    textos_limpos = [re.sub(r"[^\w\s]", "", t.lower()) for t in textos]


    elogios = ["bom", "ótimo", "excelente", "maravilhoso", "adoro", "recomendo"]
    criticas = ["ruim", "péssimo", "demorado", "caro", "não gostei", "problema"]
    sugestoes = ["poderia", "deveria", "sugiro", "seria melhor", "melhorar"]


    contagem_elogios = sum(any(p in t for p in elogios) for t in textos_limpos)
    contagem_criticas = sum(any(p in t for p in criticas) for t in textos_limpos)
    contagem_sugestoes = sum(any(p in t for p in sugestoes) for t in textos_limpos)


    palavras = " ".join(textos_limpos).split()
    top_palavras = Counter(palavras).most_common(5)
    temas = ", ".join([p[0] for p in top_palavras])


    resumo = f"""
    Foram analisadas {len(df)} avaliações.  
    Identificamos {contagem_elogios} elogios, {contagem_criticas} críticas e {contagem_sugestoes} sugestões.  
    Os temas mais recorrentes incluem: {temas}.  
    Recomenda-se atenção especial aos pontos críticos e valorização dos aspectos positivos percebidos pelos clientes.
    """
    return resumo

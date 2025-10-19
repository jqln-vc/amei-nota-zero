import pandas as pd
import json
import os
from transformers import pipeline
#from file_loader import load_file
import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
#from langchain.chains import ConversationalRetrievalChain
from pydantic import BaseModel, Field


# API KEY
load_dotenv()
if "GROQ_API_KEY" not in os.environ:
    groq_key = st.secrets.get("GROQ_API_KEY")
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
        
# MODELS
llm_model = "llama-3.3-70b-versatile"
sent_model = "cardiffnlp/xlm-roberta-base-tweet-sentiment-pt"
sent_nlp = pipeline("sentiment-analysis", model=sent_model, device=-1)

# PROMPT ENGINEERING
prompt_template = """
Com base no CONTEXTO a seguir, extraia as informações solicitadas, e retorne apenas o objeto.
NÃO INCLUA nenhuma informação ou texto antes ou depois do JSON.
NÃO INCLUA nenhuma informação que não esteja no CONTEXTO.
O conteúdo pode estar em diversas línguas, mas a saída deve ser sempre em PORTUGUÊS BRASILEIRO.

-- INÍCIO DO CONTEXTO --
{context}
-- FIM DO CONTEXTO --

INSTRUÇÕES DE FORMATAÇÃO:
{format_instructions}

"""

class SummaryStruct(BaseModel):
    summary: str = Field(description="Um resumo sobre as avaliações, inclua os elogios e reclamações mais frequentes.")
    key_topics: list[str] = Field(description="Uma lista de 3 a 5 tópicos principais contidos nas avaliações.")
    advice: str = Field(description="Considere todas as avaliações e pense em uma sugestão para melhorar imediatamente.")


with open("data/iavv_google_reviews.json", "r", encoding="utf-8") as f:
    data = json.load(f)

column_data = [
    "name",
    "review_text",
    "reviews_per_score_1",
    "reviews_per_score_2",
    "reviews_per_score_3",
    "reviews_per_score_4",
    "reviews_per_score_5"
]
df = pd.DataFrame(data, columns=column_data)

df["sent_analysis_raw"] = df["review_text"].dropna().apply(sent_nlp)
df["sent_tag"] = df["sent_analysis_raw"].str[0].str["label"]
df["sent_score"] = df["sent_analysis_raw"].str[0].str["score"]
print(df["sent_analysis_raw"])
print(df["sent_tag"])
print(df["sent_score"])

review_list = df["review_text"].dropna().astype(str).tolist()
all_reviews = " ".join(review_list)

@st.cache_resource
def process_reviews(data: str) -> "SummaryStruct":
    """"""
    llm = ChatGroq(model_name=llm_model, temperature=0)
    parser = JsonOutputParser(pydantic_object=SummaryStruct)
    
    prompt = ChatPromptTemplate.from_template(
        template = prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    summary_chain = prompt | llm | parser
    extracted_info = summary_chain.invoke({"context": data})

    return extracted_info

extracted_info = process_reviews(all_reviews)

print(extracted_info)



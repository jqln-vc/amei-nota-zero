"""
Testes unitários para o módulo funcionalidades/nlp.py

Testa a estrutura do modelo SummaryStruct (Pydantic) e a função
de extração de sentimento, além das configurações de prompt e modelos.
"""

import unittest
from unittest.mock import MagicMock
import sys
import os
import pandas as pd

# Mock das dependências externas antes de importar o módulo nlp
sys.modules["transformers"] = MagicMock()
sys.modules["dotenv"] = MagicMock()
sys.modules["langchain_core"] = MagicMock()
sys.modules["langchain_core.output_parsers"] = MagicMock()
sys.modules["langchain_groq"] = MagicMock()
sys.modules["langchain_core.prompts"] = MagicMock()

os.environ["GROQ_API_KEY"] = "fake_key_for_testing"

sys.modules["transformers"].pipeline = MagicMock()

import streamlit as st
st.cache_resource = lambda func=None, **kwargs: (lambda f: f) if func is None else func

from funcionalidades.nlp import (
    SummaryStruct,
    extrair_sentimento,
    prompt_template,
    llm_model,
    sent_model,
)


class TestSummaryStruct(unittest.TestCase):
    """Testes para o modelo Pydantic SummaryStruct."""

    def test_criacao_summary_struct(self):
        struct = SummaryStruct(
            summary="Resumo de teste",
            key_topics=["Atendimento", "Preço"],
            advice="Melhorar atendimento",
        )
        self.assertEqual(struct.summary, "Resumo de teste")
        self.assertEqual(len(struct.key_topics), 2)
        self.assertEqual(struct.advice, "Melhorar atendimento")

    def test_summary_struct_campos_obrigatorios(self):
        with self.assertRaises(Exception):
            SummaryStruct()

    def test_key_topics_e_lista(self):
        struct = SummaryStruct(
            summary="Teste",
            key_topics=["A", "B", "C", "D"],
            advice="Conselho",
        )
        self.assertIsInstance(struct.key_topics, list)
        self.assertEqual(len(struct.key_topics), 4)

    def test_summary_e_string(self):
        struct = SummaryStruct(
            summary="Um resumo",
            key_topics=["Tópico"],
            advice="Conselho",
        )
        self.assertIsInstance(struct.summary, str)

    def test_advice_e_string(self):
        struct = SummaryStruct(
            summary="Resumo",
            key_topics=["Tópico"],
            advice="Melhore o atendimento",
        )
        self.assertIsInstance(struct.advice, str)

    def test_key_topics_com_cinco_itens(self):
        struct = SummaryStruct(
            summary="Resumo",
            key_topics=["A", "B", "C", "D", "E"],
            advice="Conselho",
        )
        self.assertEqual(len(struct.key_topics), 5)


class TestExtrairSentimento(unittest.TestCase):
    """Testes para a função extrair_sentimento."""

    def setUp(self):
        from funcionalidades import nlp
        nlp.sent_nlp = lambda x: [{"label": "Positive", "score": 0.95}]

    def test_extrair_sentimento_retorna_tupla(self):
        df = pd.DataFrame({"review_text": ["Ótimo produto!", "Muito ruim"]})
        resultado = extrair_sentimento(df)
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)

    def test_extrair_sentimento_retorna_dataframe_e_string(self):
        df = pd.DataFrame({"review_text": ["Bom produto"]})
        df_result, all_reviews = extrair_sentimento(df)
        self.assertIsInstance(df_result, pd.DataFrame)
        self.assertIsInstance(all_reviews, str)

    def test_extrair_sentimento_cria_coluna_sent_tag(self):
        df = pd.DataFrame({"review_text": ["Bom"]})
        df_result, _ = extrair_sentimento(df)
        self.assertIn("sent_tag", df_result.columns)

    def test_extrair_sentimento_cria_coluna_sent_score(self):
        df = pd.DataFrame({"review_text": ["Ruim"]})
        df_result, _ = extrair_sentimento(df)
        self.assertIn("sent_score", df_result.columns)

    def test_extrair_sentimento_remove_coluna_raw(self):
        df = pd.DataFrame({"review_text": ["Okay"]})
        df_result, _ = extrair_sentimento(df)
        self.assertNotIn("sent_analysis_raw", df_result.columns)

    def test_all_reviews_concatena_textos(self):
        df = pd.DataFrame({"review_text": ["Bom", "Ótimo"]})
        _, all_reviews = extrair_sentimento(df)
        self.assertIn("Bom", all_reviews)
        self.assertIn("Ótimo", all_reviews)


class TestPromptTemplate(unittest.TestCase):
    """Testes para a configuração do prompt template."""

    def test_prompt_contem_contexto(self):
        self.assertIn("{context}", prompt_template)

    def test_prompt_contem_format_instructions(self):
        self.assertIn("{format_instructions}", prompt_template)

    def test_prompt_em_portugues(self):
        self.assertIn("PORTUGUÊS BRASILEIRO", prompt_template)

    def test_prompt_contem_instrucoes_json(self):
        self.assertIn("JSON", prompt_template)


class TestModelConfig(unittest.TestCase):
    """Testes para a configuração dos modelos."""

    def test_modelo_llm(self):
        self.assertEqual(llm_model, "llama-3.3-70b-versatile")

    def test_modelo_sentimento(self):
        self.assertIn("sentiment", sent_model)

    def test_modelo_sentimento_portugues(self):
        self.assertIn("pt", sent_model)


if __name__ == "__main__":
    unittest.main()

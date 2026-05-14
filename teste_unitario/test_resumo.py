"""
Testes unitários para o módulo funcionalidades/resumo.py

Testa a função de exibição do resumo inteligente com base nos dados
carregados e no tema visual selecionado.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd


class TestExibirResumo(unittest.TestCase):
    """Testes para a função exibir_resumo."""

    @patch("funcionalidades.resumo.st")
    def test_exibe_info_quando_df_none(self, mock_st):
        from funcionalidades.resumo import exibir_resumo
        exibir_resumo(None, "Claro")
        mock_st.info.assert_called_once_with("Aguardando dados para gerar o resumo.")

    @patch("funcionalidades.resumo.st")
    def test_exibe_info_quando_df_vazio(self, mock_st):
        from funcionalidades.resumo import exibir_resumo
        df_vazio = pd.DataFrame()
        exibir_resumo(df_vazio, "Claro")
        mock_st.info.assert_called_once()

    @patch("funcionalidades.resumo.st")
    def test_exibe_resumo_com_dados_tema_claro(self, mock_st):
        from funcionalidades.resumo import exibir_resumo
        df = pd.DataFrame({"Sentimento": ["Positivo", "Negativo", "Neutro"]})
        exibir_resumo(df, "Claro")
        chamadas_markdown = mock_st.markdown.call_args_list
        self.assertTrue(len(chamadas_markdown) >= 2)
        conteudo_html = chamadas_markdown[-1][0][0]
        self.assertIn("#222222", conteudo_html)

    @patch("funcionalidades.resumo.st")
    def test_exibe_resumo_com_dados_tema_escuro(self, mock_st):
        from funcionalidades.resumo import exibir_resumo
        df = pd.DataFrame({"Sentimento": ["Positivo"]})
        exibir_resumo(df, "Escuro")
        chamadas_markdown = mock_st.markdown.call_args_list
        conteudo_html = chamadas_markdown[-1][0][0]
        self.assertIn("#FFFFFF", conteudo_html)

    @patch("funcionalidades.resumo.st")
    def test_resumo_contem_insights(self, mock_st):
        from funcionalidades.resumo import exibir_resumo
        df = pd.DataFrame({"Sentimento": ["Positivo", "Negativo"]})
        exibir_resumo(df, "Claro")
        chamadas_markdown = mock_st.markdown.call_args_list
        conteudo_html = chamadas_markdown[-1][0][0]
        self.assertIn("Principais Insights", conteudo_html)

    @patch("funcionalidades.resumo.st")
    def test_resumo_contem_recomendacao(self, mock_st):
        from funcionalidades.resumo import exibir_resumo
        df = pd.DataFrame({"Sentimento": ["Positivo"]})
        exibir_resumo(df, "Claro")
        chamadas_markdown = mock_st.markdown.call_args_list
        conteudo_html = chamadas_markdown[-1][0][0]
        self.assertIn("Recomendação Estratégica", conteudo_html)

    @patch("funcionalidades.resumo.st")
    def test_resumo_titulo_correto(self, mock_st):
        from funcionalidades.resumo import exibir_resumo
        df = pd.DataFrame({"Sentimento": ["Positivo"]})
        exibir_resumo(df, "Claro")
        primeira_chamada = mock_st.markdown.call_args_list[0][0][0]
        self.assertIn("Resumo Inteligente", primeira_chamada)

    @patch("funcionalidades.resumo.st")
    def test_resumo_usa_unsafe_allow_html(self, mock_st):
        from funcionalidades.resumo import exibir_resumo
        df = pd.DataFrame({"Sentimento": ["Positivo"]})
        exibir_resumo(df, "Claro")
        chamadas = mock_st.markdown.call_args_list
        ultima_chamada = chamadas[-1]
        self.assertTrue(ultima_chamada[1].get("unsafe_allow_html", False))


if __name__ == "__main__":
    unittest.main()

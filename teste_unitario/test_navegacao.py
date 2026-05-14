"""
Testes unitários para o módulo componentes/navegacao.py

Testa a função de configuração de navegação da barra lateral.
"""

import unittest
from unittest.mock import patch, MagicMock


class TestConfigurarNavegacao(unittest.TestCase):
    """Testes para a função configurar_navegacao."""

    @patch("componentes.navegacao.st")
    def test_retorna_opcao_selecionada(self, mock_st):
        mock_st.session_state = {"modo_tema": "Claro"}
        mock_st.sidebar.radio.return_value = "Início"
        from componentes.navegacao import configurar_navegacao
        resultado = configurar_navegacao()
        self.assertEqual(resultado, "Início")

    @patch("componentes.navegacao.st")
    def test_opcoes_de_navegacao(self, mock_st):
        mock_st.session_state = {"modo_tema": "Claro"}
        mock_st.sidebar.radio.return_value = "Início"
        from componentes.navegacao import configurar_navegacao
        configurar_navegacao()
        chamada = mock_st.sidebar.radio.call_args
        opcoes = chamada[1].get("options") or chamada[0][1] if len(chamada[0]) > 1 else chamada[1].get("options")
        self.assertIn("Início", opcoes)
        self.assertIn("Análise de Avaliações", opcoes)

    @patch("componentes.navegacao.st")
    def test_usa_cor_tema_claro(self, mock_st):
        mock_st.session_state = {"modo_tema": "Claro"}
        mock_st.sidebar.radio.return_value = "Início"
        from componentes.navegacao import configurar_navegacao
        configurar_navegacao()
        chamada_markdown = mock_st.sidebar.markdown.call_args
        self.assertIn("#222222", chamada_markdown[0][0])

    @patch("componentes.navegacao.st")
    def test_usa_cor_tema_escuro(self, mock_st):
        mock_st.session_state = {"modo_tema": "Escuro"}
        mock_st.sidebar.radio.return_value = "Início"
        from componentes.navegacao import configurar_navegacao
        configurar_navegacao()
        chamada_markdown = mock_st.sidebar.markdown.call_args
        self.assertIn("#FFFFFF", chamada_markdown[0][0])

    @patch("componentes.navegacao.st")
    def test_tema_padrao_quando_nao_definido(self, mock_st):
        mock_session = MagicMock()
        mock_session.get.return_value = "claro"
        mock_st.session_state = mock_session
        mock_st.sidebar.radio.return_value = "Início"
        from componentes.navegacao import configurar_navegacao
        configurar_navegacao()
        mock_st.sidebar.markdown.assert_called_once()

    @patch("componentes.navegacao.st")
    def test_retorna_analise_avaliacoes(self, mock_st):
        mock_st.session_state = {"modo_tema": "Claro"}
        mock_st.sidebar.radio.return_value = "Análise de Avaliações"
        from componentes.navegacao import configurar_navegacao
        resultado = configurar_navegacao()
        self.assertEqual(resultado, "Análise de Avaliações")


if __name__ == "__main__":
    unittest.main()

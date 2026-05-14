"""
Testes unitários para o módulo funcionalidades/visualizacao.py

Testa a função de geração de gráficos com Altair, verificando
a correta configuração de cores, dados e temas.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd


class TestGerarGraficoAltair(unittest.TestCase):
    """Testes para a função gerar_grafico_altair."""

    @patch("funcionalidades.visualizacao.alt")
    @patch("funcionalidades.visualizacao.st")
    def test_gera_grafico_tema_claro(self, mock_st, mock_alt):
        mock_chart = MagicMock()
        mock_bars = MagicMock()
        mock_text = MagicMock()
        mock_combined = MagicMock()

        mock_alt.Chart.return_value.mark_bar.return_value.encode.return_value = mock_bars
        mock_bars.mark_text.return_value.encode.return_value = mock_text
        mock_bars.__add__ = MagicMock(return_value=mock_combined)
        mock_combined.properties.return_value.configure.return_value.configure_view.return_value = mock_chart

        from funcionalidades.visualizacao import gerar_grafico_altair
        df = pd.DataFrame({"Sentimento": ["Elogios"] * 5})
        gerar_grafico_altair(df, "Claro")
        mock_st.altair_chart.assert_called_once()

    @patch("funcionalidades.visualizacao.alt")
    @patch("funcionalidades.visualizacao.st")
    def test_gera_grafico_tema_escuro(self, mock_st, mock_alt):
        mock_chart = MagicMock()
        mock_bars = MagicMock()
        mock_text = MagicMock()
        mock_combined = MagicMock()

        mock_alt.Chart.return_value.mark_bar.return_value.encode.return_value = mock_bars
        mock_bars.mark_text.return_value.encode.return_value = mock_text
        mock_bars.__add__ = MagicMock(return_value=mock_combined)
        mock_combined.properties.return_value.configure.return_value.configure_view.return_value = mock_chart

        from funcionalidades.visualizacao import gerar_grafico_altair
        df = pd.DataFrame({"Sentimento": ["Elogios"] * 5})
        gerar_grafico_altair(df, "Escuro")
        mock_st.altair_chart.assert_called_once()

    @patch("funcionalidades.visualizacao.alt")
    @patch("funcionalidades.visualizacao.st")
    def test_cor_texto_claro(self, mock_st, mock_alt):
        mock_bars = MagicMock()
        mock_text = MagicMock()
        mock_combined = MagicMock()

        mock_alt.Chart.return_value.mark_bar.return_value.encode.return_value = mock_bars
        mock_bars.mark_text.return_value.encode.return_value = mock_text
        mock_bars.__add__ = MagicMock(return_value=mock_combined)
        mock_combined.properties.return_value.configure.return_value.configure_view.return_value = MagicMock()

        from funcionalidades.visualizacao import gerar_grafico_altair
        df = pd.DataFrame({"Sentimento": ["Elogios"]})
        gerar_grafico_altair(df, "Claro")

        mock_alt.value.assert_called_with("#222222")

    @patch("funcionalidades.visualizacao.alt")
    @patch("funcionalidades.visualizacao.st")
    def test_cor_texto_escuro(self, mock_st, mock_alt):
        mock_bars = MagicMock()
        mock_text = MagicMock()
        mock_combined = MagicMock()

        mock_alt.Chart.return_value.mark_bar.return_value.encode.return_value = mock_bars
        mock_bars.mark_text.return_value.encode.return_value = mock_text
        mock_bars.__add__ = MagicMock(return_value=mock_combined)
        mock_combined.properties.return_value.configure.return_value.configure_view.return_value = MagicMock()

        from funcionalidades.visualizacao import gerar_grafico_altair
        df = pd.DataFrame({"Sentimento": ["Elogios"]})
        gerar_grafico_altair(df, "Escuro")

        mock_alt.value.assert_called_with("#FFFFFF")

    @patch("funcionalidades.visualizacao.alt")
    @patch("funcionalidades.visualizacao.st")
    def test_altair_chart_sem_tema(self, mock_st, mock_alt):
        mock_bars = MagicMock()
        mock_text = MagicMock()
        mock_combined = MagicMock()
        mock_final = MagicMock()

        mock_alt.Chart.return_value.mark_bar.return_value.encode.return_value = mock_bars
        mock_bars.mark_text.return_value.encode.return_value = mock_text
        mock_bars.__add__ = MagicMock(return_value=mock_combined)
        mock_combined.properties.return_value.configure.return_value.configure_view.return_value = mock_final

        from funcionalidades.visualizacao import gerar_grafico_altair
        df = pd.DataFrame({"Sentimento": ["Elogios"]})
        gerar_grafico_altair(df, "Claro")

        chamada = mock_st.altair_chart.call_args
        self.assertIsNone(chamada[1].get("theme"))

    @patch("funcionalidades.visualizacao.alt")
    @patch("funcionalidades.visualizacao.st")
    def test_dados_do_grafico_contem_categorias(self, mock_st, mock_alt):
        mock_bars = MagicMock()
        mock_text = MagicMock()
        mock_combined = MagicMock()

        mock_alt.Chart.return_value.mark_bar.return_value.encode.return_value = mock_bars
        mock_bars.mark_text.return_value.encode.return_value = mock_text
        mock_bars.__add__ = MagicMock(return_value=mock_combined)
        mock_combined.properties.return_value.configure.return_value.configure_view.return_value = MagicMock()

        from funcionalidades.visualizacao import gerar_grafico_altair
        df = pd.DataFrame({"Sentimento": ["Elogios"]})
        gerar_grafico_altair(df, "Claro")

        chamada_data = mock_alt.Data.call_args
        valores = chamada_data[1].get("values") or chamada_data[0][0]
        categorias = [v["Categoria"] for v in valores]
        self.assertIn("Elogios", categorias)
        self.assertIn("Sugestões", categorias)
        self.assertIn("Críticas", categorias)


if __name__ == "__main__":
    unittest.main()

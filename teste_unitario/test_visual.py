"""
Testes unitários para o módulo estilos/visual.py

Testa as funções de estilização visual da aplicação, incluindo
paleta de cores, cor de texto por tema e exibição de avisos.
"""

import unittest
from unittest.mock import patch, MagicMock


class TestObterPaleta(unittest.TestCase):
    """Testes para a função obter_paleta."""

    def test_retorna_dicionario(self):
        from estilos.visual import obter_paleta
        resultado = obter_paleta("Claro")
        self.assertIsInstance(resultado, dict)

    def test_contem_chaves_esperadas(self):
        from estilos.visual import obter_paleta
        resultado = obter_paleta("Claro")
        self.assertIn("Elogios", resultado)
        self.assertIn("Sugestões", resultado)
        self.assertIn("Criticas", resultado)

    def test_cores_sao_strings_hex(self):
        from estilos.visual import obter_paleta
        resultado = obter_paleta("Claro")
        for cor in resultado.values():
            self.assertTrue(cor.startswith("#"), f"Cor {cor} não é hexadecimal")

    def test_elogios_cor_verde(self):
        from estilos.visual import obter_paleta
        resultado = obter_paleta("Claro")
        self.assertEqual(resultado["Elogios"], "#009E73")

    def test_sugestoes_cor_amarela(self):
        from estilos.visual import obter_paleta
        resultado = obter_paleta("Claro")
        self.assertEqual(resultado["Sugestões"], "#E69F00")

    def test_criticas_cor_vermelha(self):
        from estilos.visual import obter_paleta
        resultado = obter_paleta("Claro")
        self.assertEqual(resultado["Criticas"], "#D55E00")

    def test_paleta_independente_do_tema(self):
        from estilos.visual import obter_paleta
        paleta_claro = obter_paleta("Claro")
        paleta_escuro = obter_paleta("Escuro")
        self.assertEqual(paleta_claro, paleta_escuro)

    def test_paleta_tem_tres_categorias(self):
        from estilos.visual import obter_paleta
        resultado = obter_paleta("Claro")
        self.assertEqual(len(resultado), 3)


class TestCorTextoTema(unittest.TestCase):
    """Testes para a função cor_texto_tema."""

    def test_tema_claro_retorna_cor_escura(self):
        from estilos.visual import cor_texto_tema
        self.assertEqual(cor_texto_tema("Claro"), "#222222")

    def test_tema_escuro_retorna_cor_branca(self):
        from estilos.visual import cor_texto_tema
        self.assertEqual(cor_texto_tema("Escuro"), "#FFFFFF")

    def test_tema_claro_minusculo(self):
        from estilos.visual import cor_texto_tema
        self.assertEqual(cor_texto_tema("claro"), "#222222")

    def test_tema_claro_com_espacos(self):
        from estilos.visual import cor_texto_tema
        self.assertEqual(cor_texto_tema("  Claro  "), "#222222")

    def test_tema_escuro_minusculo(self):
        from estilos.visual import cor_texto_tema
        self.assertEqual(cor_texto_tema("escuro"), "#FFFFFF")

    def test_tema_desconhecido_retorna_branco(self):
        from estilos.visual import cor_texto_tema
        resultado = cor_texto_tema("outro")
        self.assertEqual(resultado, "#FFFFFF")


class TestAplicarEstilos(unittest.TestCase):
    """Testes para a função aplicar_estilos."""

    @patch("estilos.visual.st")
    def test_aplica_estilos_tema_claro(self, mock_st):
        mock_st.session_state = {}
        from estilos.visual import aplicar_estilos
        aplicar_estilos("Padrão", "Claro")
        mock_st.markdown.assert_called_once()
        chamada = mock_st.markdown.call_args
        self.assertIn("<style>", chamada[0][0])

    @patch("estilos.visual.st")
    def test_aplica_estilos_tema_escuro(self, mock_st):
        mock_st.session_state = {}
        from estilos.visual import aplicar_estilos
        aplicar_estilos("Padrão", "Escuro")
        mock_st.markdown.assert_called_once()
        chamada = mock_st.markdown.call_args
        self.assertIn("#0E1117", chamada[0][0])

    @patch("estilos.visual.st")
    def test_tamanho_fonte_padrao(self, mock_st):
        mock_st.session_state = {}
        from estilos.visual import aplicar_estilos
        aplicar_estilos("Padrão", "Claro")
        chamada = mock_st.markdown.call_args
        self.assertIn("16px", chamada[0][0])

    @patch("estilos.visual.st")
    def test_tamanho_fonte_grande(self, mock_st):
        mock_st.session_state = {}
        from estilos.visual import aplicar_estilos
        aplicar_estilos("Grande", "Claro")
        chamada = mock_st.markdown.call_args
        self.assertIn("18px", chamada[0][0])

    @patch("estilos.visual.st")
    def test_tamanho_fonte_extra_grande(self, mock_st):
        mock_st.session_state = {}
        from estilos.visual import aplicar_estilos
        aplicar_estilos("Extra Grande", "Claro")
        chamada = mock_st.markdown.call_args
        self.assertIn("22px", chamada[0][0])

    @patch("estilos.visual.st")
    def test_tamanho_fonte_desconhecido_usa_padrao(self, mock_st):
        mock_st.session_state = {}
        from estilos.visual import aplicar_estilos
        aplicar_estilos("Desconhecido", "Claro")
        chamada = mock_st.markdown.call_args
        self.assertIn("16px", chamada[0][0])

    @patch("estilos.visual.st")
    def test_cor_texto_salva_no_session_state(self, mock_st):
        mock_st.session_state = {}
        from estilos.visual import aplicar_estilos
        aplicar_estilos("Padrão", "Claro")
        self.assertEqual(mock_st.session_state["cor_texto_dinamico"], "#222222")


class TestMostrarAviso(unittest.TestCase):
    """Testes para a função mostrar_aviso."""

    @patch("estilos.visual.st")
    def test_mostra_aviso_tema_claro(self, mock_st):
        from estilos.visual import mostrar_aviso
        mostrar_aviso("Mensagem de teste", "Claro")
        mock_st.markdown.assert_called_once()
        chamada = mock_st.markdown.call_args
        self.assertIn("Mensagem de teste", chamada[0][0])
        self.assertIn("#222222", chamada[0][0])

    @patch("estilos.visual.st")
    def test_mostra_aviso_tema_escuro(self, mock_st):
        from estilos.visual import mostrar_aviso
        mostrar_aviso("Alerta escuro", "Escuro")
        chamada = mock_st.markdown.call_args
        self.assertIn("Alerta escuro", chamada[0][0])
        self.assertIn("#FFFFFF", chamada[0][0])

    @patch("estilos.visual.st")
    def test_aviso_contem_borda_vermelha(self, mock_st):
        from estilos.visual import mostrar_aviso
        mostrar_aviso("Teste", "Claro")
        chamada = mock_st.markdown.call_args
        self.assertIn("#FF4B4B", chamada[0][0])

    @patch("estilos.visual.st")
    def test_aviso_unsafe_allow_html(self, mock_st):
        from estilos.visual import mostrar_aviso
        mostrar_aviso("Teste", "Claro")
        chamada = mock_st.markdown.call_args
        self.assertTrue(chamada[1].get("unsafe_allow_html", False))


if __name__ == "__main__":
    unittest.main()

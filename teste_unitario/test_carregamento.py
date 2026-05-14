"""
Testes unitários para o módulo funcionalidades/carregamento.py

Testa as funções de carregamento de arquivos (CSV, Excel, JSON, TXT)
e exibição de dados.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import io


class TestCarregarArquivo(unittest.TestCase):
    """Testes para a função carregar_arquivo."""

    @patch("funcionalidades.carregamento.st")
    def test_retorna_none_sem_arquivo(self, mock_st):
        mock_st.file_uploader.return_value = None
        from funcionalidades.carregamento import carregar_arquivo
        resultado = carregar_arquivo()
        self.assertIsNone(resultado)

    @patch("funcionalidades.carregamento.st")
    def test_carrega_csv(self, mock_st):
        conteudo_csv = "coluna1,coluna2\nvalor1,valor2\nvalor3,valor4"
        arquivo_mock = MagicMock()
        arquivo_mock.name = "dados.csv"
        arquivo_mock.read.return_value = conteudo_csv.encode("utf-8")
        arquivo_mock.seek = MagicMock()

        mock_st.file_uploader.return_value = arquivo_mock

        with patch("funcionalidades.carregamento.pd.read_csv") as mock_read_csv:
            df_esperado = pd.DataFrame({"coluna1": ["valor1", "valor3"], "coluna2": ["valor2", "valor4"]})
            mock_read_csv.return_value = df_esperado

            from funcionalidades.carregamento import carregar_arquivo
            resultado = carregar_arquivo()

            mock_read_csv.assert_called_once_with(arquivo_mock)
            self.assertIsNotNone(resultado)
            pd.testing.assert_frame_equal(resultado, df_esperado)

    @patch("funcionalidades.carregamento.st")
    def test_carrega_xlsx(self, mock_st):
        arquivo_mock = MagicMock()
        arquivo_mock.name = "dados.xlsx"
        mock_st.file_uploader.return_value = arquivo_mock

        with patch("funcionalidades.carregamento.pd.read_excel") as mock_read_excel:
            df_esperado = pd.DataFrame({"col": [1, 2, 3]})
            mock_read_excel.return_value = df_esperado

            from funcionalidades.carregamento import carregar_arquivo
            resultado = carregar_arquivo()

            mock_read_excel.assert_called_once_with(arquivo_mock)
            pd.testing.assert_frame_equal(resultado, df_esperado)

    @patch("funcionalidades.carregamento.st")
    def test_carrega_json(self, mock_st):
        arquivo_mock = MagicMock()
        arquivo_mock.name = "dados.json"
        mock_st.file_uploader.return_value = arquivo_mock

        with patch("funcionalidades.carregamento.pd.read_json") as mock_read_json:
            df_esperado = pd.DataFrame({"nome": ["Ana", "João"]})
            mock_read_json.return_value = df_esperado

            from funcionalidades.carregamento import carregar_arquivo
            resultado = carregar_arquivo()

            mock_read_json.assert_called_once_with(arquivo_mock)
            pd.testing.assert_frame_equal(resultado, df_esperado)

    @patch("funcionalidades.carregamento.st")
    def test_carrega_txt_como_tsv(self, mock_st):
        arquivo_mock = MagicMock()
        arquivo_mock.name = "dados.txt"
        mock_st.file_uploader.return_value = arquivo_mock

        with patch("funcionalidades.carregamento.pd.read_csv") as mock_read_csv:
            df_esperado = pd.DataFrame({"col": ["a", "b"]})
            mock_read_csv.return_value = df_esperado

            from funcionalidades.carregamento import carregar_arquivo
            resultado = carregar_arquivo()

            mock_read_csv.assert_called_once_with(arquivo_mock, sep='\t')
            pd.testing.assert_frame_equal(resultado, df_esperado)

    @patch("funcionalidades.carregamento.st")
    def test_erro_ao_ler_arquivo_retorna_none(self, mock_st):
        arquivo_mock = MagicMock()
        arquivo_mock.name = "dados.csv"
        mock_st.file_uploader.return_value = arquivo_mock

        with patch("funcionalidades.carregamento.pd.read_csv", side_effect=Exception("Erro de leitura")):
            from funcionalidades.carregamento import carregar_arquivo
            resultado = carregar_arquivo()

            self.assertIsNone(resultado)
            mock_st.error.assert_called_once()

    @patch("funcionalidades.carregamento.st")
    def test_file_uploader_aceita_tipos_corretos(self, mock_st):
        mock_st.file_uploader.return_value = None
        from funcionalidades.carregamento import carregar_arquivo
        carregar_arquivo()
        chamada = mock_st.file_uploader.call_args
        tipos = chamada[1].get("type") or chamada[0][1] if len(chamada[0]) > 1 else chamada[1].get("type")
        self.assertIn("csv", tipos)
        self.assertIn("xlsx", tipos)
        self.assertIn("txt", tipos)
        self.assertIn("json", tipos)


class TestExibirDados(unittest.TestCase):
    """Testes para a função exibir_dados."""

    @patch("funcionalidades.carregamento.st")
    def test_exibe_dados_com_dataframe(self, mock_st):
        from funcionalidades.carregamento import exibir_dados
        df = pd.DataFrame({"coluna": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]})
        exibir_dados(df)
        mock_st.write.assert_called()
        mock_st.dataframe.assert_called_once()

    @patch("funcionalidades.carregamento.st")
    def test_nao_exibe_dados_com_none(self, mock_st):
        from funcionalidades.carregamento import exibir_dados
        exibir_dados(None)
        mock_st.dataframe.assert_not_called()

    @patch("funcionalidades.carregamento.st")
    def test_exibe_head_10(self, mock_st):
        from funcionalidades.carregamento import exibir_dados
        df = pd.DataFrame({"coluna": range(20)})
        exibir_dados(df)
        chamada_dataframe = mock_st.dataframe.call_args[0][0]
        self.assertEqual(len(chamada_dataframe), 10)


if __name__ == "__main__":
    unittest.main()

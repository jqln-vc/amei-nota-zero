"""
Testes unitários para o módulo funcionalidades/user_crud.py

Testa as funções de CRUD (Create, Read, Update, Delete) para
operações com banco de dados SQLite via Streamlit.
"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
import pandas as pd


class TestSalvarAvaliacoes(unittest.TestCase):
    """Testes para a função salvar_avaliacoes."""

    @patch("funcionalidades.user_crud.st")
    def test_salva_dataframe_com_sucesso(self, mock_st):
        from funcionalidades.user_crud import salvar_avaliacoes

        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_conn.engine = mock_engine

        df = pd.DataFrame({"avaliacao": ["Ótimo", "Ruim"], "nota": [5, 1]})
        salvar_avaliacoes(df, mock_conn)

        mock_st.success.assert_called_once_with("Dados salvos com sucesso!")

    @patch("funcionalidades.user_crud.st")
    def test_exibe_erro_quando_falha(self, mock_st):
        from funcionalidades.user_crud import salvar_avaliacoes

        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_conn.engine = mock_engine

        df = MagicMock()
        df.to_sql.side_effect = Exception("Erro no banco")

        salvar_avaliacoes(df, mock_conn)
        mock_st.error.assert_called_once()

    @patch("funcionalidades.user_crud.st")
    def test_usa_replace_para_tabela_existente(self, mock_st):
        from funcionalidades.user_crud import salvar_avaliacoes

        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_conn.engine = mock_engine

        df = pd.DataFrame({"coluna": [1]})
        with patch.object(pd.DataFrame, "to_sql") as mock_to_sql:
            salvar_avaliacoes(df, mock_conn)
            chamada = mock_to_sql.call_args
            self.assertEqual(chamada[1].get("if_exists"), "replace")

    @patch("funcionalidades.user_crud.st")
    def test_nome_tabela_avaliacoes(self, mock_st):
        from funcionalidades.user_crud import salvar_avaliacoes

        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_conn.engine = mock_engine

        df = pd.DataFrame({"coluna": [1]})
        with patch.object(pd.DataFrame, "to_sql") as mock_to_sql:
            salvar_avaliacoes(df, mock_conn)
            chamada = mock_to_sql.call_args
            self.assertEqual(chamada[1].get("name"), "avaliacoes")

    @patch("funcionalidades.user_crud.st")
    def test_sem_indice_ao_salvar(self, mock_st):
        from funcionalidades.user_crud import salvar_avaliacoes

        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_conn.engine = mock_engine

        df = pd.DataFrame({"coluna": [1]})
        with patch.object(pd.DataFrame, "to_sql") as mock_to_sql:
            salvar_avaliacoes(df, mock_conn)
            chamada = mock_to_sql.call_args
            self.assertFalse(chamada[1].get("index", True))


class TestCarregarAvaliacoes(unittest.TestCase):
    """Testes para a função carregar_avaliacoes."""

    @patch("funcionalidades.user_crud.st")
    def test_executa_query_select(self, mock_st):
        from funcionalidades.user_crud import carregar_avaliacoes

        mock_conn = MagicMock()
        df_esperado = pd.DataFrame({"avaliacao": ["Bom"], "nota": [4]})
        mock_conn.query.return_value = df_esperado

        resultado = carregar_avaliacoes(mock_conn)
        mock_conn.query.assert_called_once_with("SELECT * FROM avaliacoes")

    @patch("funcionalidades.user_crud.st")
    def test_retorna_dataframe(self, mock_st):
        from funcionalidades.user_crud import carregar_avaliacoes

        mock_conn = MagicMock()
        df_esperado = pd.DataFrame({"avaliacao": ["Bom"], "nota": [4]})
        mock_conn.query.return_value = df_esperado

        resultado = carregar_avaliacoes(mock_conn)
        pd.testing.assert_frame_equal(resultado, df_esperado)


class TestConectarBanco(unittest.TestCase):
    """Testes para a função conectar_banco."""

    @patch("funcionalidades.user_crud.st")
    def test_conectar_banco_chama_connection(self, mock_st):
        mock_conn = MagicMock()
        mock_st.connection.return_value = mock_conn
        mock_st.cache_resource = lambda func: func

        from funcionalidades.user_crud import conectar_banco
        try:
            resultado = conectar_banco()
        except Exception:
            pass
        mock_st.connection.assert_called()


if __name__ == "__main__":
    unittest.main()

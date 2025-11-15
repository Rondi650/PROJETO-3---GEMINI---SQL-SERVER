
import sys
import importlib
from unittest.mock import patch, MagicMock


def test_get_database_connection():
    # Garante import limpo para disparar o create_engine no import
    sys.modules.pop("app.core.database", None)

    with patch("sqlalchemy.create_engine") as mock_ce:
        mock_engine = MagicMock()
        mock_ce.return_value = mock_engine

        database = importlib.import_module("app.core.database")

        # create_engine foi chamado ao importar o módulo
        mock_ce.assert_called_once()
        # engine do módulo é o retornado pelo create_engine patchado
        assert database.engine is mock_engine
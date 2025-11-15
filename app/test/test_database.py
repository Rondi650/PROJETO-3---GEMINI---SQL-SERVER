from unittest.mock import patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_get_database_connection():
    with patch("app.core.database.create_engine") as mock_ce:
        from app.core import database
        _ = database.engine  # acessa engine (já criado ao importar)
        mock_ce.assert_called_once()


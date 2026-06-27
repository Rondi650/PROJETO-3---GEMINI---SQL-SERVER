import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "rag.db")

def get_connection():
    """Retorna uma conexão com o banco SQLite."""
    # Garante que o diretório data existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Cria a tabela de histórico de chat se não existir."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS HistoricoChat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            mensagem TEXT,
            origem TEXT,
            data_hora TEXT,
            model TEXT
        )
        """
        cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()

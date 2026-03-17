import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='rondi',
        password='rondi',
        database='RAG',
        port=3306
    )

def create_table():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            CREATE TABLE IF NOT EXISTS HistoricoChat (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(100),
                mensagem TEXT,
                origem VARCHAR(20),
                data_hora DATETIME,
                model VARCHAR(100)
            )
            """
            cursor.execute(sql)
            conn.commit()
    finally:
        conn.close()

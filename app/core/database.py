from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from app.core.config import DATABASE_URL
 
# Crie a URL de conexão
connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": DATABASE_URL}
)
 
# Cria o engine (motor de conexão com SQL Server)
engine = create_engine(connection_url)
 
# SessionLocal é uma fábrica de sessões (conexões com o banco)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
 
# Crie a URL de conexão
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=IA;Trusted_Connection=yes;"
connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": connection_string}
)
 
# Cria o engine (motor de conexão com SQL Server)
engine = create_engine(connection_url)
 
# SessionLocal é uma fábrica de sessões (conexões com o banco)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
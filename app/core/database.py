from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from app.core.config import DATABASE_URL
 
def _create_engine_from_env(db_url: str):
    # 1) SQLite (ex.: sqlite:///... ou sqlite:////...)
    if db_url.startswith("sqlite"):
        # check_same_thread=False para Gradio/threads
        return create_engine(db_url, connect_args={"check_same_thread": False})
    # 2) URL SQLAlchemy completa (ex.: mssql+pyodbc://..., postgresql://..., etc.)
    if "://" in db_url and db_url.split("://", 1)[0]:
        return create_engine(db_url)
    # 3) String ODBC pura (LOCAL_SQLSERVER do .env)
    return create_engine(
        URL.create("mssql+pyodbc", query={"odbc_connect": db_url})
    )

# Cria o engine de forma dinâmica conforme DATABASE_URL
engine = _create_engine_from_env(DATABASE_URL)

# SessionLocal é uma fábrica de sessões (conexões com o banco)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

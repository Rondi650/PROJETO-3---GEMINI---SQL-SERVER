from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from app.core.config import DATABASE_URL
from app.models.chat import Base
 
def _create_engine_from_env(db_url: str):
    # 1) SQLite (ex.: sqlite:///... ou sqlite:////...)
    if db_url.startswith("sqlite"):
        # check_same_thread=False para Gradio/threads
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        return engine
    # 2) URL SQLAlchemy completa (ex.: mssql+pyodbc://..., postgresql://..., etc.)
    if "://" in db_url and db_url.split("://", 1)[0]:
        engine = create_engine(db_url)
        Base.metadata.create_all(bind=engine)
        return engine
    # 3) String ODBC pura (LOCAL_SQLSERVER do .env)
    engine = create_engine(URL.create("mssql+pyodbc", query={"odbc_connect": db_url}))
    Base.metadata.create_all(bind=engine)
    return engine

# Cria o engine de forma dinâmica conforme DATABASE_URL
engine = _create_engine_from_env(DATABASE_URL)

# SessionLocal é uma fábrica de sessões (conexões com o banco)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

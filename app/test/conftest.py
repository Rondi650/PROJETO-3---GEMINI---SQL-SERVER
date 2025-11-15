import pytest
from datetime import datetime
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.core.database import SessionLocal
from app.models.chat import Base
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat

        
@pytest.fixture
def db_session():
    """Cria sessão de banco em memória para testes."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def chat_repository(db_session):
    """Retorna repositório de chat com sessão de teste."""
    return ChatRepository(db_session)


@pytest.fixture
def mensagem_usuario():
    """Fixture de mensagem de usuário padrão."""
    return MensagemChat(
        usuario="TestUser",
        mensagem="Olá, bot!",
        origem="usuario",
        data_hora=datetime.now(),
        model="gpt-4o-mini"
    )


@pytest.fixture
def mensagem_bot():
    """Fixture de mensagem de bot padrão."""
    return MensagemChat(
        usuario="Assistente",
        mensagem="Olá! Como posso ajudar?",
        origem="bot",
        data_hora=datetime.now(),
        model="gpt-4o-mini"
    )


@pytest.fixture
def mock_openai_response():
    """Mock de resposta da OpenAI."""
    return "Esta é uma resposta mockada do modelo de IA."


@pytest.fixture
def historico_mensagens():
    """Fixture com histórico de mensagens."""
    return [
        {"role": "user", "content": "Primeira pergunta"},
        {"role": "assistant", "content": "Primeira resposta"},
        {"role": "user", "content": "Segunda pergunta"},
        {"role": "assistant", "content": "Segunda resposta"},
    ]
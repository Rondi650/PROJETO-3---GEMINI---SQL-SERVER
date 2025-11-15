import pytest
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat
from app.core.database import *
from app.models.chat import Base

@pytest.fixture
def repo_mem():
    eng = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(eng)
    Session = sessionmaker(bind=eng)
    s = Session()
    yield ChatRepository(s)
    s.close()
    Base.metadata.drop_all(eng)

class TestIntegracaoCompleta:
    def test_fluxo_completo_salvamento_mensagens(self, repo_mem):
        msgs = [
            MensagemChat(usuario="User", mensagem="Olá", origem="usuario", data_hora=datetime.now(), model="m"),
            MensagemChat(usuario="Bot", mensagem="Oi!", origem="bot", data_hora=datetime.now(), model="m"),
            MensagemChat(usuario="User", mensagem="Me explique RAG", origem="usuario", data_hora=datetime.now(), model="m"),
        ]
        for m in msgs:
            repo_mem.salvar_mensagem(m)
        hist = repo_mem.obter_historico()
        assert len(hist) == 3
        assert hist[0].mensagem == "Olá"
        assert hist[1].origem == "bot"
        assert hist[2].mensagem == "Me explique RAG"
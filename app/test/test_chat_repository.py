import pytest
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.schemas.chat import MensagemChat
from app.repositories.chat_repository import ChatRepository
from app.core.database import SessionLocal

class TestChatRepository:
    db = SessionLocal()
    chat_repository = ChatRepository(db)
    """Suite de testes para ChatRepository."""

    def test_salvar_mensagem_usuario(self, chat_repository, mensagem_usuario):
        """Testa salvamento de mensagem de usuário."""
        chat_repository.salvar_mensagem(mensagem_usuario)
        historico = chat_repository.obter_historico()
        
        assert len(historico) == 1
        assert historico[0].usuario == "TestUser"
        assert historico[0].mensagem == "Olá, bot!"
        assert historico[0].origem == "usuario"

    def test_salvar_mensagem_bot(self, chat_repository, mensagem_bot):
        """Testa salvamento de mensagem do bot."""
        chat_repository.salvar_mensagem(mensagem_bot)
        historico = chat_repository.obter_historico()
        
        assert len(historico) == 1
        assert historico[0].usuario == "Assistente"
        assert historico[0].origem == "bot"

    def test_obter_historico_vazio(self, chat_repository):
        """Testa obtenção de histórico quando não há mensagens."""
        historico = chat_repository.obter_historico()
        assert len(historico) == 0

    def test_obter_historico_multiplas_mensagens(self, chat_repository, mensagem_usuario, mensagem_bot):
        """Testa obtenção de histórico com múltiplas mensagens."""
        chat_repository.salvar_mensagem(mensagem_usuario)
        chat_repository.salvar_mensagem(mensagem_bot)
        
        historico = chat_repository.obter_historico()
        assert len(historico) == 2

    def test_obter_historico_filtrado_por_usuario(self, chat_repository):
        """Testa filtragem de histórico por usuário."""
        msg1 = MensagemChat(
            usuario="User1",
            mensagem="Msg 1",
            origem="usuario",
            data_hora=datetime.now(),
            model="gpt-4o-mini"
        )
        msg2 = MensagemChat(
            usuario="User2",
            mensagem="Msg 2",
            origem="usuario",
            data_hora=datetime.now(),
            model="gpt-4o-mini"
        )
        
        chat_repository.salvar_mensagem(msg1)
        chat_repository.salvar_mensagem(msg2)
        
        historico = chat_repository.obter_historico(usuario="User1")
        assert len(historico) == 1
        assert historico[0].usuario == "User1"

    def test_ordem_cronologica_historico(self, chat_repository):
        """Testa se histórico está em ordem cronológica."""
        import time
        
        msg1 = MensagemChat(
            usuario="User",
            mensagem="Primeira",
            origem="usuario",
            data_hora=datetime.now(),
            model="gpt-4o-mini"
        )
        time.sleep(0.01)  # Garante timestamps diferentes
        
        msg2 = MensagemChat(
            usuario="User",
            mensagem="Segunda",
            origem="usuario",
            data_hora=datetime.now(),
            model="gpt-4o-mini"
        )
        
        chat_repository.salvar_mensagem(msg1)
        chat_repository.salvar_mensagem(msg2)
        
        historico = chat_repository.obter_historico()
        assert historico[0].mensagem == "Primeira"
        assert historico[1].mensagem == "Segunda"

    def test_rollback_em_erro(self, chat_repository, monkeypatch):
        """Testa rollback quando ocorre erro ao salvar."""
        def mock_commit_error():
            raise Exception("Erro simulado")
        
        monkeypatch.setattr(chat_repository.db, "commit", mock_commit_error)
        
        mensagem = MensagemChat(
            usuario="Test",
            mensagem="Test",
            origem="usuario",
            data_hora=datetime.now(),
            model="gpt-4o-mini"
        )
        
        # Não deve lançar exceção, apenas fazer rollback
        chat_repository.salvar_mensagem(mensagem)
        
        # Verifica que nada foi salvo
        historico = chat_repository.obter_historico()
        assert len(historico) == 0
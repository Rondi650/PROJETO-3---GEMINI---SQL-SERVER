import pytest
from datetime import datetime
from pydantic import ValidationError
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.schemas.chat import MensagemChat


class TestMensagemChat:
    """Testes do schema MensagemChat."""

    def test_criar_mensagem_valida(self):
        """Testa criação de mensagem válida."""
        msg = MensagemChat(
            usuario="TestUser",
            mensagem="Hello",
            origem="usuario",
            data_hora=datetime.now(),
            model="gpt-4o-mini"
        )
        
        assert msg.usuario == "TestUser"
        assert msg.mensagem == "Hello"
        assert msg.origem == "usuario"
        assert msg.model == "gpt-4o-mini"

    def test_mensagem_vazia_invalida(self):
        """Testa que mensagem vazia é inválida."""
        with pytest.raises(ValidationError) as exc_info:
            MensagemChat(
                usuario="User",
                mensagem="   ",  # Apenas espaços
                origem="usuario",
                data_hora=datetime.now(),
                model="gpt-4o-mini"
            )
        
        # Verifica que o erro é no campo "mensagem"
        assert "mensagem" in str(exc_info.value).lower()

    def test_mensagem_string_vazia_invalida(self):
        """Testa que string vazia é inválida."""
        with pytest.raises(ValidationError):
            MensagemChat(
                usuario="User",
                mensagem="",  # String vazia
                origem="usuario",
                data_hora=datetime.now(),
                model="gpt-4o-mini"
            )

    def test_origem_invalida(self):
        """Testa validação de origem (usuario ou bot)."""
        with pytest.raises(ValidationError) as exc_info:
            MensagemChat(
                usuario="User",
                mensagem="Ok",
                origem="invalido",  # Deve ser 'usuario' ou 'bot'
                data_hora=datetime.now(),
                model="gpt-4o-mini"
            )
        
        # Verifica que o erro é no campo "origem"
        assert "origem" in str(exc_info.value).lower()

    def test_origem_usuario_valida(self):
        """Testa origem 'usuario' válida."""
        msg = MensagemChat(
            usuario="User",
            mensagem="Test",
            origem="usuario",
            data_hora=datetime.now(),
            model="gpt-4o-mini"
        )
        assert msg.origem == "usuario"

    def test_origem_bot_valida(self):
        """Testa origem 'bot' válida."""
        msg = MensagemChat(
            usuario="Bot",
            mensagem="Response",
            origem="bot",
            data_hora=datetime.now(),
            model="gpt-4o-mini"
        )
        assert msg.origem == "bot"

    def test_mensagem_com_espacos_extras_normalizada(self):
        """Testa que espaços extras são removidos."""
        msg = MensagemChat(
            usuario="  User  ",
            mensagem="  Hello World  ",
            origem="usuario",
            data_hora=datetime.now(),
            model="  gpt-4o-mini  "
        )
        
        assert msg.usuario == "User"
        assert msg.mensagem == "Hello World"
        assert msg.model == "gpt-4o-mini"

    def test_usuario_vazio_invalido(self):
        """Testa que usuário vazio é inválido."""
        with pytest.raises(ValidationError):
            MensagemChat(
                usuario="",
                mensagem="Test",
                origem="usuario",
                data_hora=datetime.now(),
                model="gpt-4o-mini"
            )

    def test_model_vazio_invalido(self):
        """Testa que model vazio é inválido."""
        with pytest.raises(ValidationError):
            MensagemChat(
                usuario="User",
                mensagem="Test",
                origem="usuario",
                data_hora=datetime.now(),
                model=""
            )
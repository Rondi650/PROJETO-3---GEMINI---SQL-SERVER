import pytest
from datetime import datetime
from pydantic import ValidationError
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.schemas.chat import MensagemChat


class TestMensagemChat:
    def test_mensagem_vazia_invalida(self):
        with pytest.raises(ValidationError):
            MensagemChat(
                usuario="User",
                mensagem="   ",
                origem="usuario",
                data_hora=datetime.now(),
                model="x"
            )

    def test_origem_invalida(self):
        with pytest.raises(ValidationError):
            MensagemChat(
                usuario="User",
                mensagem="Ok",
                origem="invalido",
                data_hora=datetime.now(),
                model="x"
            )
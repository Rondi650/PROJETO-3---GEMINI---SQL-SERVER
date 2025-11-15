import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.utils.prompt_builder import formatar_historico

class TestFormatarHistorico:
    """Suite de testes para formatar_historico."""

    def test_historico_vazio(self):
        """Testa formatação de histórico vazio."""
        resultado = formatar_historico([])
        assert resultado == ""

    def test_uma_mensagem(self):
        """Testa formatação de uma única mensagem."""
        mensagens = [{"role": "user", "content": "Olá"}]
        resultado = formatar_historico(mensagens)
        
        assert "user:" in resultado
        assert "Olá" in resultado
        assert len(resultado.splitlines()) == 1

    def test_limite_default(self, historico_mensagens):
        """Testa que limite padrão é 20 mensagens."""
        mensagens = [
            {"role": "user", "content": f"msg{i}"} for i in range(30)
        ]
        resultado = formatar_historico(mensagens)
        linhas = resultado.splitlines()
        
        assert len(linhas) == 20
        assert "msg10" in linhas[0]  # primeiras 10 foram cortadas
        assert "msg29" in linhas[-1]

    def test_limite_customizado(self):
        """Testa limite customizado de mensagens."""
        mensagens = [
            {"role": "assistant", "content": f"resp{i}"} for i in range(10)
        ]
        resultado = formatar_historico(mensagens, limite=5)
        linhas = resultado.splitlines()
        
        assert len(linhas) == 5
        assert "resp5" in linhas[0]
        assert "resp9" in linhas[-1]

    def test_alternancia_user_assistant(self):
        """Testa formatação com alternância de roles."""
        mensagens = [
            {"role": "user", "content": "Pergunta 1"},
            {"role": "assistant", "content": "Resposta 1"},
            {"role": "user", "content": "Pergunta 2"},
            {"role": "assistant", "content": "Resposta 2"},
        ]
        resultado = formatar_historico(mensagens)
        linhas = resultado.splitlines()
        
        assert len(linhas) == 4
        assert linhas[0] == "user: Pergunta 1"
        assert linhas[1] == "assistant: Resposta 1"
        assert linhas[2] == "user: Pergunta 2"
        assert linhas[3] == "assistant: Resposta 2"

    def test_system_message_incluido(self):
        """Testa inclusão de system message."""
        mensagens = [
            {"role": "system", "content": "Você é um assistente."},
            {"role": "user", "content": "Olá"},
        ]
        resultado = formatar_historico(mensagens)
        
        assert "system: Você é um assistente." in resultado
        assert "user: Olá" in resultado

    def test_limite_menor_que_mensagens(self):
        """Testa comportamento quando limite é maior que número de mensagens."""
        mensagens = [
            {"role": "user", "content": "msg1"},
            {"role": "user", "content": "msg2"},
        ]
        resultado = formatar_historico(mensagens, limite=100)
        linhas = resultado.splitlines()
        
        assert len(linhas) == 2

    @pytest.mark.parametrize("role,conteudo", [
        ("user", "Teste user"),
        ("assistant", "Teste assistant"),
        ("system", "Teste system"),
    ])
    def test_diferentes_roles(self, role, conteudo):
        """Testa formatação de diferentes tipos de roles."""
        mensagens = [{"role": role, "content": conteudo}]
        resultado = formatar_historico(mensagens)
        
        assert f"{role}: {conteudo}" in resultado
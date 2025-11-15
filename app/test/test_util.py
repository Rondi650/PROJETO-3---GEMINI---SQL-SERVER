from app.utils.prompt_builder import formatar_historico
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def test_formatar_historico_limite_default():
    mensagens = [
        {"role": "user", "content": f"m{i}"} for i in range(30)
    ]
    out = formatar_historico(mensagens)  # limite padrão = 20
    linhas = out.splitlines()
    assert len(linhas) == 20
    assert linhas[0].endswith("m10")
    assert linhas[-1].endswith("m29")

def test_formatar_historico_limite_custom():
    mensagens = [
        {"role": "assistant", "content": f"a{i}"} for i in range(5)
    ]
    out = formatar_historico(mensagens, limite=3)
    linhas = out.splitlines()
    assert len(linhas) == 3
    assert linhas[0].endswith("a2")
    assert linhas[-1].endswith("a4")
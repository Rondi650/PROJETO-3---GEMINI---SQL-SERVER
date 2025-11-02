
def formatar_historico(mensagens: list[dict]) -> str:
    """Formata lista de mensagens em prompt de texto."""
    lista = []
    for msg in mensagens:
        lista.append(f"{msg['role']}: {msg['content']}")
    prompt = "\n".join(lista[-20:])  # Limitar aos últimos 20 turnos (40 mensagens)
    return prompt

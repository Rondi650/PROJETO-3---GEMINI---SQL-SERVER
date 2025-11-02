
def formatar_historico(mensagens: list[dict], limite: int = 20) -> str:
    """
    Formata lista de mensagens em prompt de texto.
    
    Args:
        mensagens: Lista de dicts com 'role' e 'content'
        limite: Número máximo de mensagens a incluir (padrão: 20)
    
    Returns:
        Prompt formatado em texto com quebras de linha
    """
    lista = []
    for msg in mensagens:
        lista.append(f"{msg['role']}: {msg['content']}")
    prompt = "\n".join(lista[-limite:])  # Limitar aos últimos 'limite' turnos
    return prompt

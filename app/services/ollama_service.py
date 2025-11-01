from ollama import chat

class OllamaService:
    def gerar_resposta(self, pergunta: str, model: str) -> str:
        try:
            messages = [
                {
                'role': 'system',
                'content': 'Voce e meu assistente virtual.'
                }
            ]
            stream = chat(
            model=model,
            messages=[*messages, {'role': 'user', 'content': pergunta}],
            options={'temperature': 0.5},
            stream=True
            )

            # Exibe resposta em tempo real
            resposta = ''
            for part in stream:
                resposta += part['message']['content']
            return resposta
        except Exception as e:
            print(f"Erro ao consultar Ollama: {e}")
            return f"Erro ao consultar Ollama: {e}"
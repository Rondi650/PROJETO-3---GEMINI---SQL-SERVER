from ollama import chat

class OllamaService:
    def gerar_resposta(self, pergunta: str, model: str, temperature: float = 1.0) -> str:
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
            options={'temperature': 1.0},
            stream=True
            )

            # Exibe resposta em tempo real
            resposta = ''
            for part in stream:
                resposta += part['message']['content']
                print(part['message']['content'], end='', flush=True)
            return resposta
        except Exception as e:
            print(f"Erro ao consultar Ollama: {e}")
            return f"Erro ao consultar Ollama: {e}"
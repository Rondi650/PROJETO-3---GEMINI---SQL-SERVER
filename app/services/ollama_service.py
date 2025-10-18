# app/services/gemini_service.py
from ollama import chat

class OllamaService:
        
    def gerar_resposta(self, pergunta: str, model: str) -> str:
        messages = [
            {
            'role': 'system',
            'content': 'Voce e meu assistente virtual Rondinho.'
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
            print(part['message']['content'], end='', flush=True)
            resposta += part['message']['content']
        print()  # Nova linha após resposta
        return resposta  # Adicione este retorno
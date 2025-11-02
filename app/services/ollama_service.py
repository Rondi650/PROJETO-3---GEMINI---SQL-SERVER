from ollama import chat

class OllamaService:
    """Serviço para comunicação com modelos Ollama locais."""
    
    def gerar_resposta(self, pergunta: str, model: str, temperature: float = 1.0) -> str:
        """
        Gera resposta usando um modelo Ollama local.
        
        Args:
            pergunta: Texto ou prompt a enviar ao modelo
            model: Nome do modelo Ollama a usar
            temperature: Controla a criatividade (0-2)
        
        Returns:
            Resposta completa do modelo como string
        """
        try:
            # Define mensagem de sistema
            messages = [
                {
                    'role': 'system',
                    'content': 'Voce e meu assistente virtual.'
                }
            ]
            
            # Chama API do Ollama com streaming
            stream = chat(
                model=model,
                messages=[*messages, {'role': 'user', 'content': pergunta}],
                options={'temperature': temperature},
                stream=True
            )

            # Acumula resposta e exibe em tempo real
            resposta = ''
            for part in stream:
                conteudo = part['message']['content']
                resposta += conteudo
                print(conteudo, end='', flush=True)
            
            return resposta
            
        except Exception as e:
            print(f"Erro ao consultar Ollama: {e}")
            return f"Erro ao consultar Ollama: {e}"

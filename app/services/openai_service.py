from openai import OpenAI
from app.core.config import OPENAI_API_KEY

class OpenAIService:
    """Serviço de integração com a API da OpenAI para geração de respostas."""
    
    def __init__(self):
        """Inicializa o cliente OpenAI com a chave de API do ambiente."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def gerar_resposta(self, pergunta: str, model: str, temperature: float = 1.0) -> str:
        """
        Gera uma resposta usando o modelo OpenAI especificado.
        
        Args:
            pergunta: Prompt/pergunta a ser enviada ao modelo
            model: Nome do modelo OpenAI (ex: gpt-4, gpt-3.5-turbo)
            temperature: Criatividade da resposta (0-2, padrão: 1.0)
        
        Returns:
            Resposta gerada pelo modelo ou mensagem de erro
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Voce e meu assistente virtual."},
                    {"role": "user", "content": pergunta}
                ],
                temperature=temperature,
            )
            # Extrai conteúdo da resposta ou retorna mensagem padrão
            texto = response.choices[0].message.content if response.choices else "Sem resposta da API."
            print(texto)
            return texto
        
        except Exception as e:
            print(f"Erro ao consultar OpenAI: {e}")
            return f"Erro ao consultar OpenAI: {e}"
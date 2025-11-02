from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

class GeminiService:
    """Serviço para comunicação com a API Gemini (Google)."""
    
    def __init__(self):
        """Inicializa o cliente Gemini com a chave de API do ambiente."""
        load_dotenv()
        self.api_key = os.getenv('GEMINI_KEY')
        self.client = genai.Client(api_key=self.api_key)
        
    def gerar_resposta(self, pergunta: str, model: str, temperature: float = 1.0) -> str:
        """
        Gera resposta usando a API Gemini.
        
        Args:
            pergunta: Texto ou prompt a enviar ao modelo
            model: Nome do modelo Gemini a usar
            temperature: Controla a criatividade (0-2)
        
        Returns:
            Resposta completa do modelo como string
        """
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=pergunta,
                config=types.GenerateContentConfig(
                    system_instruction="Voce e meu assistente virtual",
                    temperature=temperature,  # Usa o parâmetro recebido
                ),
            )
            
            # Retorna resposta ou mensagem padrão se vazia
            texto = response.text if response.text is not None else "Sem resposta da API."
            print(texto)
            return texto
        
        except Exception as e:
            print(f"Erro ao consultar Gemini: {e}")
            return f"Erro ao consultar Gemini: {e}"

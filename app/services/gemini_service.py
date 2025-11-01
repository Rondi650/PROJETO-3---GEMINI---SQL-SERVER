from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

class GeminiService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GEMINI_KEY')
        self.client = genai.Client(api_key=self.api_key)
        
    def gerar_resposta(self, pergunta: str, model: str, temperature: float = 1.0) -> str:
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=pergunta,
                config=types.GenerateContentConfig(
                    system_instruction="Voce e meu assistente virtual",
                    temperature=1.0,
                ),
            )
            texto = response.text if response.text is not None else "Sem resposta da API."
            print(texto)
            return texto
        
        except Exception as e:
            print(f"Erro ao consultar Gemini: {e}")
            return f"Erro ao consultar Gemini: {e}"
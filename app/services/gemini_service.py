# app/services/gemini_service.py
from google import genai
import os
from dotenv import load_dotenv

class GeminiService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GEMINI_KEY')
        self.client = genai.Client(api_key=self.api_key)
        
    def gerar_resposta(self, pergunta: str) -> str:
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-lite", contents=pergunta
            )
            return response.text if response.text else "Sem resposta da API."
        except Exception as e:
            return f"Erro ao consultar Gemini: {e}"
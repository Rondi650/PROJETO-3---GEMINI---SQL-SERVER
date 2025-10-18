# app/services/gemini_service.py
from google import genai
from google.genai import types
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
                model="gemini-2.5-flash",
                contents=pergunta,
                config=types.GenerateContentConfig(
                    system_instruction="Você é um analista de planejamento de Call Center",
                    temperature=0.5
                ),
            )
            texto = response.text if response.text is not None else "Sem resposta da API."
            print(texto)
            return texto
        
        except Exception as e:
            return f"Erro ao consultar Gemini: {e}"
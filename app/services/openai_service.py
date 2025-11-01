from openai import OpenAI
import os
from dotenv import load_dotenv

class OpenAIService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        
    def gerar_resposta(self, pergunta: str, model: str):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Voce e meu assistente virtual."},
                    {"role": "user", "content": pergunta}
                ],
                temperature=1,
            )
            texto = response.choices[0].message.content if response.choices else "Sem resposta da API."
            return texto
        
        except Exception as e:
            print(f"Erro ao consultar OpenAI: {e}")
            return f"Erro ao consultar OpenAI: {e}"



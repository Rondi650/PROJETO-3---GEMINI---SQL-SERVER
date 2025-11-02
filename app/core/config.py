import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

# Validação
if not GEMINI_KEY:
    raise ValueError("⚠️ GEMINI_KEY não configurada no .env")
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY não configurada no .env")
if not DATABASE_URL:
    raise ValueError("⚠️ DATABASE_URL não configurada no .env")
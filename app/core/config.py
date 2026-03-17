import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
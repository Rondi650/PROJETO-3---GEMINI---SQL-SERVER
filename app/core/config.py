import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LOCAL_SQLSERVER = os.getenv('LOCAL_SQLSERVER')

# Não quebra se faltar em ambiente Docker (opcional: só avisa)
if not GEMINI_KEY:
    print("Aviso: GEMINI_KEY não definida.")
if not OPENAI_API_KEY:
    print("Aviso: OPENAI_API_KEY não definida.")

# Estratégia:
# 1. Se DATABASE_URL estiver presente (Docker), usa.
# 2. Senão, tenta LOCAL_SQLSERVER_URL (ambiente local .env).
# 3. Senão, fallback para sqlite local.
DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("LOCAL_SQLSERVER")
    or "sqlite:///./data.db"
)

print(f"[CONFIG] Usando DATABASE_URL = {DATABASE_URL}")
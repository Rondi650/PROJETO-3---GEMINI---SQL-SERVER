import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Agora pode importar corretamente
from app.core.database import SessionLocal
from app.repositories.chat_repository import ChatRepository  # Corrigido o caminho de importação

# Criar sessão do banco de dados
db = SessionLocal()
try:
    # Criar repositório
    repo = ChatRepository(db)
    
    # Obter todo o histórico - alterar usuario muda a busca
    historico_completo = repo.obter_historico(usuario="Rondinelle")
    for mensagem in historico_completo:
        print(f"[{mensagem.data_hora}] {mensagem.usuario}: {mensagem.mensagem}")
finally:
    db.close()
from app.core.database import SessionLocal, engine
from app.services.gemini_service import GeminiService
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat
from app.models.chat import Base
from datetime import datetime

def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        gemini_service = GeminiService()
        chat_repository = ChatRepository(db)
        
        while True:
            # Interface com usuário
            entrada_usuario = input('Chat: ')
            
            # Verificar saída ANTES de processar
            if entrada_usuario.lower() == 'sair':
                print("Encerrando chat...")
                break
            
            # Processar mensagem do usuário
            mensagem_usuario = MensagemChat(
                usuario="Rondinelle",
                mensagem=entrada_usuario,
                origem="usuario",
                data_hora=datetime.now()
            )
            chat_repository.salvar_mensagem(mensagem_usuario)
            
            # Obter resposta da IA (já imprime em streaming)
            resposta = gemini_service.gerar_resposta(entrada_usuario)
            
            # Salvar resposta da IA
            mensagem_bot = MensagemChat(
                usuario="Assistente",
                mensagem=resposta,
                origem="bot",
                data_hora=datetime.now()
            )
            chat_repository.salvar_mensagem(mensagem_bot)
               
    finally:
        db.close()

if __name__ == "__main__":
    main()
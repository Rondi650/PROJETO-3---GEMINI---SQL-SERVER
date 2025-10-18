from app.core.database import SessionLocal
from app.services.gemini_service import GeminiService
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat
from datetime import datetime

def main():
    # Instanciar dependências
    db = SessionLocal()
    try:
        gemini_service = GeminiService()
        chat_repository = ChatRepository(db)
        
        # Interface com usuário
        entrada_usuario = input('Chat: ')
        
        # Processar mensagem do usuário
        mensagem_usuario = MensagemChat(
            usuario="Rondinelle",
            mensagem=entrada_usuario,
            origem="usuario",
            data_hora=datetime.now()
        )
        chat_repository.salvar_mensagem(mensagem_usuario)
        
        # Obter resposta da IA
        resposta = gemini_service.gerar_resposta(entrada_usuario)
        
        # Salvar resposta da IA
        mensagem_bot = MensagemChat(
            usuario="Assistente",
            mensagem=resposta,
            origem="bot",
            data_hora=datetime.now()
        )
        chat_repository.salvar_mensagem(mensagem_bot)
        
        print(f"Assistente: {resposta}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
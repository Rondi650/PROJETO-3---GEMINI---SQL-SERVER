import os
from app.core.database import SessionLocal, engine
from app.services.gemini_service import GeminiService
from app.services.ollama_service import OllamaService
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat
from app.models.chat import Base
from datetime import datetime

def inicializar_ambiente():
    """Limpa terminal e cria tabelas no banco."""
    os.system('cls')
    Base.metadata.create_all(bind=engine)

def main():
    # Conecta na sessão do banco de dados
    db = SessionLocal()
    try:
        # Instancia os serviços
        gemini_service = GeminiService()
        ollama_services = OllamaService()
        chat_repository = ChatRepository(db)
        
        # Loop principal
        while True:
            # Interface com usuário
            entrada_usuario = input('Chat: ')
            
            '''CONFIGURACOES'''
            model = "gemini-2.5-pro" 
            service_ativo = gemini_service  # ou gemini_service
            
            # Encerra a conversa
            if entrada_usuario.lower() == 'sair':
                print("Encerrando chat...")
                break
            
            # Processar mensagem do usuário
            mensagem_usuario = MensagemChat(
                usuario="Rondinelle",
                mensagem=entrada_usuario,
                origem="usuario",
                data_hora=datetime.now(),
                model=model
            )
            chat_repository.salvar_mensagem(mensagem_usuario)
            
            # Obter resposta da IA
            resposta = service_ativo.gerar_resposta(entrada_usuario, model=model)
            
            # Salvar resposta da IA
            mensagem_bot = MensagemChat(
                usuario="Assistente",
                mensagem=resposta,
                origem="bot",
                data_hora=datetime.now(),
                model=model
            )
            chat_repository.salvar_mensagem(mensagem_bot)
               
    finally:
        db.close()

if __name__ == "__main__":
    inicializar_ambiente()
    main()
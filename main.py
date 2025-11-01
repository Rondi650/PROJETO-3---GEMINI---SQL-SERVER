import os
from app.core.database import SessionLocal, engine
from app.services.gemini_service import GeminiService
from app.services.ollama_service import OllamaService
from app.services.openai_service import OpenAIService
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
        ollama_service = OllamaService()
        openai_service = OpenAIService()
        chat_repository = ChatRepository(db)
        
        # Loop principal
        while True:
            # Interface com usuário
            entrada_usuario = input('Chat: ')
            
            '''CONFIGURACOES'''
            model = "gpt-5-nano-2025-08-07" 
            service_ativo = openai_service
            
            # Encerra a conversa
            if entrada_usuario.lower() in ['sair', 'exit', 'quit', 'bye', 'fim', 'terminate', 'end', 'close']:
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
            resposta = service_ativo.gerar_resposta(entrada_usuario, model=model, temperature=1.0)
            
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
import os
from app.core.database import SessionLocal, engine
from app.utils.prompt_builder import formatar_historico
from app.services.gemini_service import GeminiService
from app.services.ollama_service import OllamaService
from app.services.openai_service import OpenAIService
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat
from app.models.chat import Base
from datetime import datetime

def inicializar_ambiente():
    """Limpa o terminal e cria as tabelas no banco de dados."""
    os.system('cls')
    Base.metadata.create_all(bind=engine)

def main():
    """Interface de chat em linha de comando com persistência em banco de dados."""
    db = SessionLocal()
    try:
        # Inicializa serviços de IA
        gemini_service = GeminiService()
        ollama_service = OllamaService()
        openai_service = OpenAIService()
        chat_repository = ChatRepository(db)
        
        historico = []  # Mantém histórico da conversa na memória
        
        while True:
            entrada_usuario = input('Chat: ')
            
            # Configuração do modelo e serviço ativo
            model = "gpt-5-nano-2025-08-07"
            service_ativo = openai_service
            
            # Permite sair da conversa
            if entrada_usuario.lower() in ['sair', 'exit', 'quit', 'bye', 'fim']:
                break
            
            # Adiciona mensagem do usuário ao histórico
            historico.append({
                "role": "user", 
                "content": entrada_usuario
            })

            # Formata histórico em texto para enviar ao modelo
            prompt = formatar_historico(historico)

            # Obtém resposta do modelo de IA
            resposta = service_ativo.gerar_resposta(
                prompt, 
                model=model, 
                temperature=1.0)
            
            # Adiciona resposta ao histórico
            historico.append({
                "role": "assistant", 
                "content": resposta
            })
            
            # Persiste mensagens no banco de dados
            msg_usuario = MensagemChat(
                usuario="Rondinelle", 
                mensagem=entrada_usuario, 
                origem="usuario", 
                data_hora=datetime.now(), 
                model=model
            )
            chat_repository.salvar_mensagem(msg_usuario)
            
            msg_bot = MensagemChat(
                usuario="Assistente", 
                mensagem=resposta, 
                origem="bot", 
                data_hora=datetime.now(), 
                model=model
            )
            chat_repository.salvar_mensagem(msg_bot)
            
            print(f"Bot: {resposta}\n")
               
    finally:
        db.close()

if __name__ == "__main__":
    inicializar_ambiente()
    main()

# filepath: c:\Users\rondi\Desktop\PROGRAMACAO\PROJETOS PESSOAIS\PROJETO 3 - GEMINI + SQL SERVER\app_chat.py
import gradio as gr
from datetime import datetime

from app.core.database import SessionLocal
from app.services.rag_services import RAGService
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat

# Inicializa dependências
db = SessionLocal()
rag_service = RAGService()
chat_repo = ChatRepository(db)

# Lista de modelos disponíveis
MODELOS_OPENAI = [
    "gpt-5-2025-08-07",
    "gpt-5-mini-2025-08-07",
    "gpt-5-nano-2025-08-07",
    "gpt-5.1-2025-11-13",
    "gpt-4.1-2025-04-14"
]

def responder(
    mensagem: str,
    history: list[dict[str, str]],
    arquivo = None,    
    modelo: str = "gpt-5-nano-2025-08-07"
):
    """
    Processa mensagem do usuário, obtém resposta do modelo de IA (normal ou RAG)
    e persiste no banco.
    """
    try:

        # Carrega o PDF uma única vez, quando vier arquivo novo
        if arquivo is not None:
            rag_service.carregar_documento(arquivo.name)

        resposta_completa = rag_service.rag(mensagem, model=modelo)

        # Monta lista de mensagens com contexto completo (modo padrão)
        messages = []
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": mensagem})

        # Envia resposta ao frontend
        yield resposta_completa

        # Persiste mensagem do usuário
        msg_user = MensagemChat(
            usuario="Usuario",
            mensagem=mensagem,
            origem="usuario",
            data_hora=datetime.now(),
            model=modelo # Nome explicito apenas para o RAG
        )
        chat_repo.salvar_mensagem(msg_user)

        # Persiste resposta do bot
        msg_bot = MensagemChat(
            usuario="Assistente",
            mensagem=resposta_completa,
            origem="bot",
            data_hora=datetime.now(),
            model=modelo # Nome explicito apenas para o RAG
        )
        chat_repo.salvar_mensagem(msg_bot)

    except Exception as e:
        yield f"❌ Erro: {e}"

# Interface web com Gradio
with gr.Blocks(title="Chat IA com RAG", theme=gr.themes.Soft()) as interface:
    gr.Markdown("## 🤖 Rondi's RAG")
    gr.Markdown("Chat com modelo de linguagem integrado a documentos PDF via RAG.")
    
    with gr.Row():
        # Sidebar com configurações
        with gr.Column(scale=1, min_width=300):
            gr.Markdown("### ⚙️ Configurações")
            
            modelo_dropdown = gr.Dropdown(
                choices=MODELOS_OPENAI,
                value="gpt-5-nano-2025-08-07",
                label="Modelo OpenAI",
                info="Escolha o modelo de linguagem"
            )
            
            arquivo_upload = gr.File(
                label="📄 Upload PDF ou TXT",
                file_types=[".pdf", ".txt"],
                interactive=True
            )
            
            gr.Markdown("---")
            gr.Markdown(
                "**Dica:** Carregue um PDF ou TXT antes de fazer perguntas.\n\n"
                "Modelos recomendados:\n"
                "- **gpt-5**: Mais completo e detalhado\n"
                "- **gpt-5-mini**: Rápido e objetivo\n"
                "- **gpt-5-nano**: Rápido e básico\n"
                "- **gpt-5.1**: Melhor para conversas longas\n"
                "- **gpt-4.1**: Eficiente e preciso\n" 
            )
        
        # Área principal do chat
        with gr.Column(scale=3):
            chatbot = gr.ChatInterface(
                fn=responder,
                type="messages",
                chatbot=gr.Chatbot(
                    height="70vh",
                    label="Chat",
                    container=True,
                ),
                additional_inputs=[
                    arquivo_upload,
                    modelo_dropdown
                ],
                textbox=gr.Textbox(
                    placeholder="Digite sua pergunta sobre o documento...",
                    label="Sua mensagem"
                ),
                examples=[
                    ["Faça um resumo do documento"],
                    ["Quais são os principais tópicos abordados?"],
                    ["Explique a seção sobre..."],
                ]
            )

if __name__ == "__main__":
    interface.launch(server_port=7861, show_error=True, share=True)

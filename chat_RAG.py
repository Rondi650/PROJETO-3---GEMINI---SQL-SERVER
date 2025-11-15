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


def responder(
    mensagem: str,
    history: list[dict[str, str]],
    arquivo_pdf = None         # gr.File -> tempfile
):
    """
    Processa mensagem do usuário, obtém resposta do modelo de IA (normal ou RAG)
    e persiste no banco.
    """
    try:

        # Carrega o PDF uma única vez, quando vier arquivo novo
        if arquivo_pdf is not None:
            rag_service.carregar_pdf(arquivo_pdf.name)

        resposta_completa = rag_service.rag(mensagem)

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
            model="gpt-5-nano-2025-08-07" # Nome explicito apenas para o RAG
        )
        chat_repo.salvar_mensagem(msg_user)

        # Persiste resposta do bot
        msg_bot = MensagemChat(
            usuario="Assistente",
            mensagem=resposta_completa,
            origem="bot",
            data_hora=datetime.now(),
            model="gpt-5-nano-2025-08-07" # Nome explicito apenas para o RAG
        )
        chat_repo.salvar_mensagem(msg_bot)

    except Exception as e:
        yield f"❌ Erro: {e}"

# Interface web com Gradio
with gr.Blocks(title="Chat IA com RAG", theme=gr.themes.Soft()) as interface:
    gr.Markdown("## 🤖 Rondi`s RAG")
    gr.Markdown("Chat com modelo de linguagem integrado a documentos PDF via RAG (Retrieval-Augmented Generation).")
    gr.Markdown("Carregue um PDF e faça perguntas baseadas no conteúdo do documento.")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.ChatInterface(
                fn=responder,
                type="messages",
                additional_inputs=[
                    gr.File(
                        label="PDF para RAG",
                        file_types=[".pdf"],
                        interactive=True
                    ),
                ],
                textbox=gr.Textbox(
                    placeholder="Digite sua mensagem aqui...",
                    label="Sua mensagem",
                    max_lines=5
                )
            )

if __name__ == "__main__":
    interface.launch(server_port=7861, show_error=True, share=True)

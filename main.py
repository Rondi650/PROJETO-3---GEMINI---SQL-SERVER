import gradio as gr
from datetime import datetime

from app.core.database import create_table
from app.services.rag_services import RAGService
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat

# Inicializa dependências
create_table()
rag_service = RAGService()
chat_repo = ChatRepository()


def responder(
    mensagem: str,
    history: list[dict[str, str]],
    arquivo_pdf=None
):
    """
    Processa mensagem do usuário com RAG e persiste no banco.
    """
    try:
        if arquivo_pdf is not None:
            rag_service.carregar_pdf(arquivo_pdf.name)

        resposta_completa = rag_service.rag(mensagem)

        # Envia resposta ao frontend
        yield resposta_completa

        # Persiste mensagem do usuário
        msg_user = MensagemChat(
            usuario="Usuario",
            mensagem=mensagem,
            origem="usuario",
            data_hora=datetime.now(),
            model="rag-openai"
        )
        chat_repo.salvar_mensagem(msg_user)

        # Persiste resposta do bot
        msg_bot = MensagemChat(
            usuario="Assistente",
            mensagem=resposta_completa,
            origem="bot",
            data_hora=datetime.now(),
            model="rag-openai"
        )
        chat_repo.salvar_mensagem(msg_bot)

    except Exception as e:
        yield f"Erro: {e}"


# Interface web com Gradio
with gr.Blocks(title="Chat IA", theme=gr.themes.Citrus()) as interface:
    gr.Markdown("## Rondi`s BOT - RAG")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.ChatInterface(
                fn=responder,
                additional_inputs=[
                    gr.File(
                        label="PDF para RAG",
                        file_types=[".pdf"],
                        interactive=True
                    ),
                ]
            )

if __name__ == "__main__":
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        share=True)

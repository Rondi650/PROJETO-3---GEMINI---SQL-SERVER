# filepath: c:\Users\rondi\Desktop\PROGRAMACAO\PROJETOS PESSOAIS\PROJETO 3 - GEMINI + SQL SERVER\app_chat.py
import gradio as gr
from datetime import datetime

from app.core.database import SessionLocal
from app.utils.prompt_builder import formatar_historico
from app.services.gemini_service import GeminiService
from app.services.ollama_service import OllamaService
from app.services.openai_service import OpenAIService
from app.services.rag_services import RAGService
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat

# Inicializa dependências
db = SessionLocal()
gemini = GeminiService()
ollama = OllamaService()
openai = OpenAIService()
rag_service = RAGService()
chat_repo = ChatRepository(db)


def responder(
    mensagem: str,
    history: list[dict[str, str]],
    system_message: str,
    servico: str,
    modelo: str,
    temperature: float,
    modo: str,           # "Padrão" ou "RAG (PDF + OpenAI)"
    arquivo_pdf = None         # gr.File -> tempfile
):
    """
    Processa mensagem do usuário, obtém resposta do modelo de IA (normal ou RAG)
    e persiste no banco.
    """
    try:
        # Se modo RAG, ignoramos Gemini/Ollama e usamos somente OpenAI + PDF
        if modo == "RAG (PDF + OpenAI)":
            # Carrega o PDF uma única vez, quando vier arquivo novo
            if arquivo_pdf is not None:
                rag_service.carregar_pdf(arquivo_pdf.name)

            resposta_completa = rag_service.rag(mensagem)

        else:
            # Monta lista de mensagens com contexto completo (modo padrão)
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": mensagem})

            prompt = formatar_historico(messages)

            if servico == "Gemini":
                resposta_completa = gemini.gerar_resposta(prompt, model=modelo, temperature=temperature)
            elif servico == "OpenAI":
                resposta_completa = openai.gerar_resposta(prompt, model=modelo, temperature=temperature)
            else:
                resposta_completa = ollama.gerar_resposta(prompt, model=modelo, temperature=temperature)

        # Envia resposta ao frontend
        yield resposta_completa

        # Persiste mensagem do usuário
        msg_user = MensagemChat(
            usuario="Usuario",
            mensagem=mensagem,
            origem="usuario",
            data_hora=datetime.now(),
            model=modelo,
        )
        chat_repo.salvar_mensagem(msg_user)

        # Persiste resposta do bot
        msg_bot = MensagemChat(
            usuario="Assistente",
            mensagem=resposta_completa,
            origem="bot",
            data_hora=datetime.now(),
            model=modelo,
        )
        chat_repo.salvar_mensagem(msg_bot)

    except Exception as e:
        yield f"❌ Erro: {e}"


# Lista de modelos disponíveis (modo padrão)
modelos_lista = [
    "gemma3:4b",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
    "gpt-5-nano-2025-08-07",
    "gpt-5-mini-2025-08-07"
]

# Interface web com Gradio
with gr.Blocks(title="Chat IA", theme=gr.themes.Soft()) as interface:
    gr.Markdown("## 🤖 Rondi`s BOT")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.ChatInterface(
                fn=responder,
                type="messages",
                additional_inputs=[
                    gr.Textbox(
                        value="Voce e meu assistente pessoal virtual.",
                        label="System message"
                    ),
                    gr.Radio(
                        ["Gemini", "Ollama", "OpenAI"],
                        value="OpenAI",
                        label="Serviço"
                    ),
                    gr.Dropdown(
                        choices=modelos_lista,
                        label="Modelo",
                        value="gpt-5-mini-2025-08-07"
                    ),
                    gr.Slider(
                        minimum=0,
                        maximum=2,
                        value=1.0,
                        label="Temperature"
                    ),
                    gr.Radio(
                        ["Padrão", "RAG (PDF + OpenAI)"],
                        value="Padrão",
                        label="Modo de resposta"
                    ),
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
    interface.launch(server_port=7860, show_error=True, share=True)

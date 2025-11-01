import gradio as gr
from datetime import datetime
from app.core.database import SessionLocal
from app.services.gemini_service import GeminiService
from app.services.ollama_service import OllamaService
from app.services.openai_service import OpenAIService
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat

db = SessionLocal()
gemini = GeminiService()
ollama = OllamaService()
openai = OpenAIService()
chat_repo = ChatRepository(db)

def responder(mensagem: str,history: list[dict[str, str]],system_message: str,servico: str,modelo: str, temperature: float=1.0):
    try:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": mensagem})
        
        # Formata para texto (embutido)
        linhas = [f"{msg.get('role')}: {msg.get('content', '')}" for msg in messages]
        prompt = "\n".join(linhas)
        
        if servico == "Gemini":
            resposta_completa = gemini.gerar_resposta(prompt, model=modelo, temperature=temperature)
        elif servico == "OpenAI":
            resposta_completa = openai.gerar_resposta(prompt, model=modelo, temperature=temperature)
        else:
            resposta_completa = ollama.gerar_resposta(prompt, model=modelo, temperature=temperature)

        yield resposta_completa
        
        msg_user = MensagemChat(
            usuario="Usuario",
            mensagem=mensagem,
            origem="usuario",
            data_hora=datetime.now(),
            model=modelo,
        )
        chat_repo.salvar_mensagem(msg_user)

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

# Interface Gradio

modelos_lista = [
"gemma3:4b",
"gemini-2.5-flash-lite",
"gemini-2.0-flash-lite",
"gpt-5-nano-2025-08-07",
"gpt-5-mini-2025-08-07"
]

chatbot = gr.ChatInterface(
    fn=responder,           # recebe (message, history, *additional_inputs) nessa ordem
    type="messages",
    additional_inputs=[
        gr.Textbox(value="Voce e meu assistente pessoal virtual.", label="System message"),
        gr.Radio(["Gemini", "Ollama", "OpenAI"], value="OpenAI", label="Serviço"),
        gr.Dropdown(choices=modelos_lista, label="Modelo", value="gpt-5-mini-2025-08-07"),
        gr.Slider(minimum=0, maximum=2, value=1.0, label="Temperature")
    ],
    textbox=gr.Textbox(
        placeholder="Digite sua mensagem aqui...",
        label="Sua mensagem",
        max_lines=5
    )
)
    
with gr.Blocks(title="Chat IA", theme=gr.themes.Soft()) as interface:
    gr.Markdown("## Rondi`s BOT")
    chatbot.render()

if __name__ == "__main__":
    interface.launch(server_port=7860, show_error=True, share=True)
    
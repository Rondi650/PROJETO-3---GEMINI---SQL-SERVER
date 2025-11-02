import gradio as gr
from datetime import datetime
from app.core.database import SessionLocal
from app.utils.prompt_builder import formatar_historico
from app.services.gemini_service import GeminiService
from app.services.ollama_service import OllamaService
from app.services.openai_service import OpenAIService
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat

# Inicializa dependências
db = SessionLocal()
gemini = GeminiService()
ollama = OllamaService()
openai = OpenAIService()
chat_repo = ChatRepository(db)

def responder(mensagem: str, 
    history: list[dict[str, str]], 
    system_message: str, 
    servico: str, 
    modelo: str, 
    temperature: float = 1.0):
    """
    Processa mensagem do usuário, obtém resposta do modelo de IA e persiste no banco.
    
    Args:
        mensagem: Mensagem atual do usuário
        history: Histórico de conversas anteriores
        system_message: Instrução de sistema para o modelo
        servico: Serviço de IA selecionado (Gemini, OpenAI, Ollama)
        modelo: Modelo de IA específico
        temperature: Criatividade da resposta (0-2)
    
    Yields:
        Resposta do modelo de IA em tempo real
    """
    try:
        # Monta lista de mensagens com contexto completo
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": mensagem})
        
        # Formata mensagens em texto para envio ao modelo
        prompt = formatar_historico(messages)
        
        # Seleciona serviço de IA e obtém resposta
        if servico == "Gemini":
            resposta_completa = gemini.gerar_resposta(prompt, model=modelo, temperature=temperature)
        elif servico == "OpenAI":
            resposta_completa = openai.gerar_resposta(prompt, model=modelo, temperature=temperature)
        else:
            resposta_completa = ollama.gerar_resposta(prompt, model=modelo, temperature=temperature)

        # Envia resposta ao frontend (streaming)
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

# Lista de modelos disponíveis
modelos_lista = [
    "gemma3:4b",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
    "gpt-5-nano-2025-08-07",
    "gpt-5-mini-2025-08-07"
]

# Configuração da interface de chat
chatbot = gr.ChatInterface(
    fn=responder,
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

# Interface web com Gradio
with gr.Blocks(title="Chat IA", theme=gr.themes.Soft()) as interface:
    gr.Markdown("## 🤖 Rondi`s BOT")
    chatbot.render()

if __name__ == "__main__":
    interface.launch(server_port=7860, show_error=True, share=True)

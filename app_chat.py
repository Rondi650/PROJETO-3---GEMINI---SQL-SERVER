import gradio as gr
from datetime import datetime
from app.core.database import SessionLocal
from app.services.gemini_service import GeminiService
from app.services.ollama_service import OllamaService
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import MensagemChat

db = SessionLocal()
gemini = GeminiService()
ollama = OllamaService()
chat_repo = ChatRepository(db)

def responder(mensagem: str,history: list[dict[str, str]],system_message: str,servico: str,modelo: str,):
    print("Mensagem recebida:", mensagem)
    print("Serviço selecionado:", servico)
    print("Modelo selecionado:", modelo)
    print("System message:", system_message)
    print("Histórico de mensagens:", history)
    print("Iniciando resposta...\n")
    try:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": mensagem})
        print("Mensagens para o modelo:", messages)
        print()
        
        # Formata para texto (embutido)
        linhas = [f"{msg.get('role')}: {msg.get('content', '')}" for msg in messages]
        prompt = "\n".join(linhas)
        
        if servico == "Gemini":
            resposta_completa = gemini.gerar_resposta(prompt, model=modelo)
        else:
            resposta_completa = ollama.gerar_resposta(prompt, model=modelo)
        print("Resposta do modelo:", resposta_completa)
        
        acumulado = ""
        for token in resposta_completa.split():
            acumulado += token + " "
            yield acumulado
            
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
with gr.Blocks(title="Chat IA", theme=gr.themes.Soft()) as interface:
    gr.Markdown("## Rondi`s BOT")

    with gr.Row():
        servico = gr.Radio(["Gemini", "Ollama"], value="Ollama", label="Serviço")
        modelo = gr.Textbox(value="gemma3:4b", label="Modelo")

    chatbot = gr.ChatInterface(
        fn=responder,           # recebe (message, history, *additional_inputs) nessa ordem
        type="messages",
        additional_inputs=[
            gr.Textbox(value="You are a friendly Chatbot and your name is Rondi.", label="System message"),
            servico,
            modelo,
        ],
    )

if __name__ == "__main__":
    interface.launch(server_port=7860, show_error=True, share=True)
    
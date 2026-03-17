# 🤖 Rondi's BOT

Um assistente de IA conversacional que integra múltiplos modelos de linguagem (Gemini, OpenAI, Ollama) com interface web interativa e persistência de histórico em banco de dados SQL Server.

## 📋 Status

🚧 **Em Desenvolvimento** - Funcionalidades de RAG (Retrieval-Augmented Generation) em progresso.

## ✨ Funcionalidades

- 💬 Chat em tempo real com suporte a streaming
- 🔄 Histórico de conversas persistente (SQL Server)
- 🤖 Suporte a múltiplos modelos de IA:
  - **Gemini** (Google)
  - **OpenAI** (GPT)
  - **Ollama** (Local)
- ⚙️ Controle de temperatura e system messages
- 🎨 Interface web com Gradio

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.10+
- SQL Server
- Chaves de API (Gemini, OpenAI)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/PROJETO-3-GEMINI-SQL-SERVER.git
cd "PROJETO 3 - GEMINI + SQL SERVER"

# Crie um ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

### Configuração

1. Crie um arquivo `.env` na raiz do projeto:
```env
GEMINI_KEY=sua_chave_aqui
OPENAI_API_KEY=sua_chave_aqui
DATABASE_URL=mssql+pyodbc://user:password@servidor/banco
```

2. Execute as migrações:
```bash
python main.py
```

## 💻 Como Usar

### Interface Web (Gradio)
```bash
python app_chat.py
```
Acesse `http://localhost:7860` no navegador.

### Terminal
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
app/
├── core/           # Configurações de banco de dados
├── repositories/   # Acesso a dados com SQL puro
├── schemas/        # Schemas de validação
├── services/       # Serviços de IA (Gemini, OpenAI, Ollama)
app_chat.py         # Interface Gradio
main.py             # Interface de linha de comando
```

## 🔜 Próximas Funcionalidades

- ✅ RAG (Retrieval-Augmented Generation)
- ✅ Upload de documentos
- ✅ Busca semântica
- ✅ Suporte a múltiplas conversas

## 👤 Autor

Rondinelle

---

**Nota:** Este projeto ainda está em desenvolvimento.q
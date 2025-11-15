# 🤖 Rondi's BOT

Um assistente de IA conversacional que integra múltiplos modelos (Gemini, OpenAI, Ollama) com interface web, modo RAG (documentos) e histórico em SQL Server.

## 📋 Status
🚧 Em desenvolvimento – RAG, Docker e ajustes de conexão em evolução.

## ✨ Funcionalidades
- 💬 Chat em tempo real (streaming) com Gradio
- 🔎 RAG: perguntas sobre PDFs/TXTs (upload e contexto)
- 🗂️ Histórico persistente (SQL Server)
- 🤖 Múltiplos provedores: Gemini, OpenAI, Ollama
- ⚙️ System message, temperature e seleção de modelos
- 🖥️ Modo Terminal (CLI)

## 🚀 Início Rápido

### Pré‑requisitos
- Python 3.10+
- SQL Server (local ou via Docker)
- Chaves de API (Gemini, OpenAI)

### Instalação
```bash
git clone https://github.com/seu-usuario/PROJETO-3-GEMINI-SQL-SERVER.git
cd "PROJETO 3 - GEMINI + SQL SERVER"

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### Configuração
Crie um arquivo .env na raiz:
```env
GEMINI_KEY=SuaChaveAqui
OPENAI_API_KEY=SuaChaveAqui
# Exemplo de URL (SQLAlchemy + pyodbc):
DATABASE_URL=mssql+pyodbc://sa:SenhaForte@123@localhost:1433/IA?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no
```

## 💻 Como Usar

### 1) Interface Web (chat padrão)
```bash
python chat_gradio.py
# Acesse: http://localhost:7860
```

### 2) Interface Web (RAG – documentos)
```bash
python chat_RAG.py
# Acesse: http://localhost:7861
```

### 3) Terminal (CLI)
```bash
python chat_terminal.py
```

### (Opcional) Via Docker
```bash
docker-compose up -d
# Web: http://localhost:7860 (chat)
# RAG: http://localhost:7861 (documentos)
```

## 📁 Estrutura do Projeto
```
app/
├── core/           # Config e conexão com banco
├── models/         # Modelos SQLAlchemy
├── repositories/   # Repositórios de dados
├── schemas/        # Schemas de validação
├── services/       # Serviços (Gemini, OpenAI, Ollama, RAG)
└── test/           # Testes
chat_gradio.py      # UI web (chat)
chat_RAG.py         # UI web (RAG)
chat_terminal.py    # Chat por terminal
Dockerfile          # Build da app
docker-compose.yml  # Orquestração (app + SQL Server)
```

## 🔜 Próximas Funcionalidades
- Melhorias no RAG e no gerenciamento de documentos
- Ajustes do Docker


## 👤 Autor
Rondinelle

---
**Nota:** Projeto em evolução; quebras de compatibilidade podem ocorrer.
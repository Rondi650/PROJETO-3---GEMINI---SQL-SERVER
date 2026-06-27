# AGENTS.md - Rondi's BOT RAG

## Project Overview
RAG chatbot with Gradio web UI, LangChain, OpenAI, FAISS vector store, and SQLite persistence.

## Architecture
```
main.py (Gradio UI)
  ├─ RAGService (app/services/rag_services.py) - RAG pipeline
  ├─ ChatRepository (app/repositories/chat_repository.py) - DB persistence
  └─ create_table() (app/core/database.py) - SQLite table setup
```

## Critical Setup Requirements

### 1. SQLite Database (File-based)
Database is stored in `data/rag.db` (auto-created on startup):
- No external server required
- File-based storage in project root
- Table auto-created via `create_table()`

### 2. OpenAI API Key
Set in `.env` file (already present):
```
OPENAI_API_KEY=sk-...
```

## Running the Application

### Local Development
```bash
# Ensure virtualenv is activated
source .venv/bin/activate

# Run the app
python main.py
```

### Docker
```bash
docker-compose up --build
```
Exposes port `7860`.

## RAG Pipeline Details

### Document Processing (`RAGService.carregar_pdf()`)
1. PDF loaded via `PyPDFLoader`
2. Split into 1000-char chunks (200 overlap)
3. Embeddings via `OpenAIEmbeddings(model="text-embedding-3-small")`
4. Stored in FAISS in-memory vectorstore
5. Retriever fetches top-3 relevant chunks

### Model Configuration
- LLM: `gpt-5-nano-2025-08-07`
- Temperature: `0.2`
- Retrieved chunks are logged to console for debugging

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Gradio UI entry point |
| `app/services/rag_services.py` | RAG pipeline implementation |
| `app/core/database.py` | SQLite connection (file-based) |
| `app/repositories/chat_repository.py` | Chat history persistence |
| `app/schemas/chat.py` | Pydantic models |
| `data/rag.db` | SQLite database file (auto-created) |

## Important Notes

- **No tests present** - this repo has no test suite
- **Vector store is in-memory** - FAISS index resets on restart
- **PDF upload required** before asking questions (RAG won't work without loaded documents)
- **SQLite database** is file-based (`data/rag.db`) and persists across restarts
- **DateTime stored as ISO format** in SQLite (converted via `.isoformat()`)

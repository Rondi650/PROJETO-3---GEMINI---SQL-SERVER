# Rondi's BOT RAG

Intelligent chatbot with RAG (Retrieval-Augmented Generation) to answer questions based on PDF documents. Web interface built with Gradio, using LangChain, OpenAI, and FAISS for natural language processing.

## What is RAG?

**RAG (Retrieval-Augmented Generation)** is a technique that combines:
- **Retrieval**: Searches for relevant information in a knowledge base
- **Augmented**: Enriches the question context with retrieved data
- **Generation**: Generates accurate answers based on the retrieved context

This allows the model to answer specific questions about documents it has never seen during training.

## How the RAG Pipeline Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Upload PDF    │────▶│  Document       │────▶│    Chunks       │
│                 │     │  Processing     │     │  (1000 chars)   │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                ┌────────────────────────┘
                                ▼
                       ┌─────────────────┐
                       │   Embeddings    │
                       │  (OpenAI text-  │
                       │ embedding-3-sm) │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Vector Store   │
                       │     FAISS       │
                       └────────┬────────┘
                                │
    Question ──────────────────▶│
                                ▼
                       ┌─────────────────┐
                       │    Retriever    │
                       │  (Top 3 chunks) │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │      LLM        │
                       │ (gpt-5-nano)    │
                       │  + Context      │
                       └────────┬────────┘
                                │
                                ▼
                          ┌──────────┐
                          │  Answer  │
                          └──────────┘
```

### Detailed Flow

#### 1. PDF Loading (`RAGService.carregar_pdf()`)
```python
# The PDF is loaded and split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Each piece has 1000 characters
    chunk_overlap=200,    # 200 characters of overlap between chunks
)
```

**Why split into chunks?**
- Language models have context limits
- Smaller chunks allow more precise search
- Overlap ensures that information is not lost at the edges

#### 2. Embedding Generation
```python
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
```

**What are embeddings?**
- Numerical vector representations of text
- Capture semantic meaning
- Similar texts are close in vector space
- Dimension: 1536 vectors per text

#### 3. Vector Storage (FAISS)
```python
vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings_model)
```

**Why FAISS?**
- Extremely fast similarity search (millions of vectors in ms)
- Efficient in-memory indexing
- Optimized algorithms for approximate nearest neighbor search (ANN)

#### 4. Context Retrieval
```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
chunks = retriever.invoke(question)
```

When the user asks a question:
1. The question is converted into an embedding
2. FAISS searches for the 3 most similar chunks (by cosine similarity)
3. These chunks form the context for the answer

#### 5. Answer Generation
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Use ONLY the context below to answer.\n\nContext:\n{context}"),
    ("human", "{question}"),
])

model = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.2)
```

The LLM receives:
- Retrieved context (top 3 chunks)
- User's question
- Instruction to use only the provided context

**Temperature = 0.2**: Generates more deterministic and focused answers

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                    (Gradio Interface)                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌──────────────┐ ┌────────┐ ┌──────────────┐
│ RAGService   │ │ Chat   │ │ create_table │
│ (Pipeline    │ │Repo    │ │   (SQLite)   │
│     RAG)     │ │        │ │              │
└──────────────┘ └────────┘ └──────────────┘
        │
   ┌────┴────┬─────────────┬─────────────┐
   │         │             │             │
   ▼         ▼             ▼             ▼
PyPDFLoader  Recursive    OpenAI       FAISS
            Character     Embeddings   Vector
            TextSplitter               Store
```

## Main Components

| Component | Technology | Function |
|-----------|------------|----------|
| **UI** | Gradio | Web interface for chat and PDF upload |
| **LLM** | OpenAI GPT-5-nano | Answer generation |
| **Embeddings** | OpenAI text-embedding-3-small | Semantic vectorization |
| **Vector Store** | FAISS | Vector storage and search |
| **Database** | SQLite | Chat history persistence |
| **PDF Parser** | PyPDFLoader | Text extraction from PDFs |

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd PROJETO-3---GEMINI---SQL-SERVER

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Edit .env with your OpenAI key
OPENAI_API_KEY=sk-your-key-here
```

## Usage

### Run locally
```bash
python main.py
```
Access: `http://localhost:7860`

### Using Docker
```bash
docker-compose up --build
```

### Usage Flow

1. **Access the web interface** in your browser
2. **Upload a PDF** using the file button
3. **Wait for processing** (document is split into chunks and indexed)
4. **Ask questions** about the document content
5. **The bot answers** based only on the loaded PDF context

## Example Interaction

```
User: [Upload of file "product_manual.pdf"]
System: PDF processed: 45 chunks created

User: What is the product warranty period?
Bot: According to the manual on page 12, the product
     has a 24-month warranty against manufacturing
     defects...

User: And how do I request the warranty?
Bot: The warranty request process described
     on page 15 requires: (1) invoice, (2)
     proof of purchase, and (3) filling out the
     online form...
```

## Configurations

### LLM Model
```python
model="gpt-5-nano-2025-08-07"
temperature=0.2
```

### Chunking
```python
chunk_size=1000      # Size of each chunk
chunk_overlap=200    # Overlap between chunks
```

### Retrieval
```python
search_kwargs={"k": 3}  # Top 3 most relevant chunks
```

## Persistence

- **Chat history**: Saved in `data/rag.db` (SQLite)
- **Vector store**: In memory (FAISS) - resets with the application
- **Documents**: Must be reloaded for each session

## Limitations

- ⚠️ **In-memory vector store**: FAISS index is lost when restarting
- ⚠️ **One PDF per session**: New upload overwrites the previous one
- ⚠️ **Limited context**: Only top 3 chunks are used per question
- ⚠️ **OpenAI dependency**: Requires valid API key

## Technologies Used

- **LangChain**: Framework for LLM applications
- **OpenAI**: Language models and embeddings
- **FAISS**: Vector search library (Facebook AI)
- **Gradio**: Web interface for ML
- **SQLite**: Lightweight embedded database
- **PyPDF**: Text extraction from PDFs

## License

This project is for educational and demonstration purposes.

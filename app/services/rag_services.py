# filepath: c:\Users\rondi\Desktop\PROGRAMACAO\PROJETOS PESSOAIS\PROJETO 3 - GEMINI + SQL SERVER\app\services\rag_service.py
from typing import Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.core.config import OPENAI_API_KEY


class RAGService:
    """
    Serviço simples de RAG usando LangChain + OpenAI + FAISS.

    Fluxo:
    - Carregar documento .txt (por enquanto)
    - Dividir em chunks
    - Gerar embeddings e criar vectorstore FAISS (em memória)
    - Usar retriever + LLM para responder perguntas
    """

    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não configurada para usar o RAG.")

        self._retriever = None
        self._chain = self._criar_chain()

    def _criar_chain(self):
        """Monta a cadeia: prompt -> modelo -> parser de string."""
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Você é um assistente que ajuda a encontrar informações em documentos.\n\n"
                "Use APENAS o contexto abaixo para responder.\n\nContexto:\n{contexto}"
            ),
            (
                "human",
                "Responda de forma clara e concisa:\n{pergunta}"
            ),
        ])

        modelo = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.2)
        print("\nModelo de linguagem inicializado.")
        return prompt | modelo | StrOutputParser()

    def carregar_pdf(self, caminho_pdf: str, encoding: str = "utf-8"):
        print("\nCarregando PDF:", caminho_pdf)
        """
        Carrega um arquivo .pdf, gera chunks e inicializa o retriever com FAISS.

        Args:
            caminho_pdf: Caminho do arquivo PDF.
            encoding: Codificação do arquivo (padrão: utf-8).
        """
        # 2. Carregar documento
        documento = PyPDFLoader(caminho_pdf).load()

        # 3. Dividir em chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        pedacos = splitter.split_documents(documento)
        print(f"\nDocumento dividido em {len(pedacos)} pedaços.")

        # 4. Embeddings + FAISS
        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
        print("\nGerando embeddings e criando vectorstore FAISS...")
        vectorstore = FAISS.from_documents(
            documents=pedacos,
            embedding=embeddings_model,
        )

        # Cria retriever (k=2 trechos mais relevantes)
        self._retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        print("\nRetriever inicializado com sucesso.")

    def rag(self, pergunta: str) -> str:
        """
        Executa o fluxo RAG: busca trechos relevantes e gera resposta.

        Args:
            pergunta: Pergunta do usuário.

        Returns:
            Resposta gerada pelo modelo com base no contexto.
        """
        if self._retriever is None:
            return "Nenhum documento foi carregado ainda. Carregue um arquivo de texto primeiro."

        # 7. Buscar trechos relevantes
        trechos = self._retriever.invoke(pergunta)
        contexto = "\n\n".join(um_trecho.page_content for um_trecho in trechos)
        for i, trecho in enumerate(trechos):
            print(f'\nTrecho encontrado {i+1}: {trecho.page_content}')
            print('-'*50)

        # 8. Gerar resposta
        resposta = self._chain.invoke({
            "pergunta": pergunta,
            "contexto": contexto,
        })
        return resposta

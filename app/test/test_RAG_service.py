import pytest
from unittest.mock import MagicMock, patch
import importlib
import os
import sys
from langchain_core.documents import Document

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class TestRAGService:
    from app.services.rag_services import RAGService
    @pytest.fixture
    def rag_service(self, monkeypatch):
        rag_mod = importlib.import_module("app.services.rag_services")
        monkeypatch.setattr(rag_mod, "OPENAI_API_KEY", "test_key")
        return rag_mod.RAGService()

    def test_inicializacao_sem_api_key(self, monkeypatch):
        rag_mod = importlib.import_module("app.services.rag_services")
        monkeypatch.setattr(rag_mod, "OPENAI_API_KEY", None)
        with pytest.raises(ValueError):
            rag_mod.RAGService()

    def test_rag_sem_documento(self, rag_service):
        r = rag_service.rag("Pergunta teste")
        assert "Nenhum documento" in r

    def test_chain_criada_com_modelo_correto(self, rag_service):
        rag_service._retriever = MagicMock()
        rag_service._retriever.invoke.return_value = []
        with patch("app.services.rag_services.ChatOpenAI") as mock_llm:
            rag_service.rag("teste")
            assert mock_llm.call_args.kwargs["model"] == "gpt-4"

    def test_chain_reutilizada_mesmo_modelo(self, rag_service):
        rag_service._retriever = MagicMock()
        rag_service._retriever.invoke.return_value = []
        with patch("app.services.rag_services.ChatOpenAI"):
            first = rag_service.rag("a")
            chain_first = rag_service._chain
            second = rag_service.rag("b")
            assert rag_service._chain is chain_first

    def test_chain_recriada_modelo_diferente(self, rag_service):
        rag_service._retriever = MagicMock()
        rag_service._retriever.invoke.return_value = []
        with patch("app.services.rag_services.ChatOpenAI"):
            rag_service.rag("a")
            c1 = rag_service._chain
            rag_service.rag("b")
            assert rag_service._chain is not c1

    @patch("app.services.rag_services.PyPDFLoader")
    @patch("app.services.rag_services.FAISS")
    def test_carregar_pdf_sucesso(self, mock_faiss, mock_loader, rag_service):
        mock_loader.return_value.load.return_value = [
            Document(page_content="Conteúdo X", metadata={"pagina": 1})
        ]
        mock_faiss.from_documents.return_value = MagicMock()
        rag_service.carregar_pdf("fake.pdf")
        assert rag_service._retriever is not None
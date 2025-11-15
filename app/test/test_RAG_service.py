import pytest
from unittest.mock import MagicMock, patch
import importlib
from langchain_core.documents import Document

class TestRAGService:
    """Suite de testes para RAGService."""

    @pytest.fixture
    def rag_service(self, monkeypatch):
        """Fixture que retorna RAGService com API key mockada."""
        rag_mod = importlib.import_module("app.services.rag_services")
        monkeypatch.setattr(rag_mod, "OPENAI_API_KEY", "test_key")
        return rag_mod.RAGService()

    def test_inicializacao_sem_api_key(self, monkeypatch):
        """Testa que RAGService falha sem API key."""
        rag_mod = importlib.import_module("app.services.rag_services")
        monkeypatch.setattr(rag_mod, "OPENAI_API_KEY", None)
        
        with pytest.raises(ValueError, match="OPENAI_API_KEY não configurada"):
            rag_mod.RAGService()

    def test_rag_sem_documento_carregado(self, rag_service):
        """Testa resposta quando nenhum documento foi carregado."""
        resposta = rag_service.rag("Qualquer pergunta")
        assert "Nenhum documento foi carregado" in resposta

    def test_chain_criada_com_modelo_correto(self, rag_service):
        """Testa que chain é criada com modelo especificado."""
        # Mock do retriever
        rag_service._retriever = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "Conteúdo teste"
        rag_service._retriever.invoke.return_value = [mock_doc]
        
        # Mock do ChatOpenAI para capturar o modelo
        with patch('app.services.rag_services.ChatOpenAI') as mock_openai:
            # Cria um mock que retorna string quando invocado
            mock_llm = MagicMock()
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = "Resposta mockada"
            
            mock_openai.return_value = mock_llm
            
            # Patch do pipe operator para retornar nossa chain mockada
            with patch('app.services.rag_services.ChatPromptTemplate') as mock_prompt:
                mock_prompt.from_messages.return_value.__or__ = lambda self, other: mock_chain.__or__(other)
                mock_chain.__or__.return_value = mock_chain
                
                # Executa
                resultado = rag_service.rag("teste", model="gpt-4")
                
                # Verifica que ChatOpenAI foi chamado com o modelo correto
                mock_openai.assert_called_once()
                call_kwargs = mock_openai.call_args.kwargs
                assert call_kwargs['model'] == "gpt-4"
                assert call_kwargs['temperature'] == 0.2

    def test_chain_reutilizada_mesmo_modelo(self, rag_service):
        """Testa que chain não é recriada quando modelo não muda."""
        # Setup
        rag_service._retriever = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "Conteúdo"
        rag_service._retriever.invoke.return_value = [mock_doc]
        
        # Mock da chain para retornar string
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Resposta teste"
        
        # Define chain e modelo manualmente
        rag_service._chain = mock_chain
        rag_service._current_model = "gpt-4o-mini"
        
        # Primeira chamada
        resultado1 = rag_service.rag("teste1", model="gpt-4o-mini")
        chain_original = rag_service._chain
        
        # Segunda chamada com mesmo modelo
        resultado2 = rag_service.rag("teste2", model="gpt-4o-mini")
        
        # Verifica que é a mesma instância
        assert rag_service._chain is chain_original
        assert mock_chain.invoke.call_count == 2

    def test_chain_recriada_modelo_diferente(self, rag_service):
        """Testa que chain é recriada quando modelo muda."""
        # Setup
        rag_service._retriever = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "Conteúdo"
        rag_service._retriever.invoke.return_value = [mock_doc]
        
        with patch.object(rag_service, '_criar_chain') as mock_criar:
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = "Resposta"
            mock_criar.return_value = mock_chain
            
            # Define modelo inicial
            rag_service._current_model = "modelo1"
            
            # Chama com modelo diferente
            rag_service.rag("teste", model="modelo2")
            
            # Verifica que _criar_chain foi chamado com novo modelo
            mock_criar.assert_called_once_with("modelo2")
            assert rag_service._current_model == "modelo2"

    @patch('app.services.rag_services.PyPDFLoader')
    @patch('app.services.rag_services.FAISS')
    @patch('app.services.rag_services.OpenAIEmbeddings')
    def test_carregar_pdf_sucesso(self, mock_embeddings, mock_faiss, mock_loader, rag_service):
        """Testa carregamento bem-sucedido de PDF."""
        # Mock do loader
        mock_loader.return_value.load.return_value = [
            Document(page_content="Conteúdo página 1", metadata={"page": 1}),
            Document(page_content="Conteúdo página 2", metadata={"page": 2})
        ]
        
        # Mock do FAISS
        mock_vectorstore = MagicMock()
        mock_retriever = MagicMock()
        mock_vectorstore.as_retriever.return_value = mock_retriever
        mock_faiss.from_documents.return_value = mock_vectorstore
        
        # Mock dos embeddings
        mock_embeddings.return_value = MagicMock()
        
        # Executa
        rag_service.carregar_documento("test.pdf")
        
        # Verifica
        assert rag_service._retriever is not None
        mock_loader.assert_called_once_with("test.pdf")
        mock_faiss.from_documents.assert_called_once()

    def test_retriever_busca_k_trechos(self, rag_service):
        """Testa que retriever busca número correto de trechos."""
        from unittest.mock import MagicMock, patch

        # Setup retriever mockado
        mock_retriever = MagicMock()
        mock_trecho1 = MagicMock(); mock_trecho1.page_content = "Trecho 1"
        mock_trecho2 = MagicMock(); mock_trecho2.page_content = "Trecho 2"
        mock_trecho3 = MagicMock(); mock_trecho3.page_content = "Trecho 3"
        mock_retriever.invoke.return_value = [mock_trecho1, mock_trecho2, mock_trecho3]
        rag_service._retriever = mock_retriever

        # Mock da chain que suporta invoke e chamada direta (__call__)
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Resposta baseada em 3 trechos"
        mock_chain.return_value = "Resposta baseada em 3 trechos"  # __call__

        # Mock do _criar_chain para retornar nossa chain mockada
        with patch.object(rag_service, "_criar_chain", return_value=mock_chain) as mock_criar:
            resultado = rag_service.rag("pergunta teste")

            mock_retriever.invoke.assert_called_once_with("pergunta teste")
            mock_criar.assert_called_once()  # chain criada

            # Aceita tanto invoke() quanto __call__()
            assert mock_chain.invoke.called or mock_chain.called

            # Captura os argumentos passados para a chain
            if mock_chain.invoke.called:
                payload = mock_chain.invoke.call_args[0][0]
            else:
                payload = mock_chain.call_args[0][0]

            assert payload["pergunta"] == "pergunta teste"
            assert "Trecho 1" in payload["contexto"]
            assert "Trecho 2" in payload["contexto"]
            assert "Trecho 3" in payload["contexto"]
            assert resultado == "Resposta baseada em 3 trechos"

from app.services.rag_services import RAGService

if __name__ == "__main__":
    rag = RAGService()
    rag.carregar_pdf('GTB_platinum_Nov23.pdf')  # ajuste o caminho
    resposta = rag.rag("Quais telefones de contato estão listados no documento?")
    print("Resposta RAG:\n", resposta)
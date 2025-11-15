import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.services.rag_services import RAGService

'''TESTE COM PDF'''
if __name__ == "__main__":
    rag = RAGService()
    rag.carregar_documento('app\\documents\\GTB_platinum_Nov23.pdf')  # ajuste o caminho
    resposta = rag.rag("Quais telefones de contato estão listados no documento?", model="gpt-5-nano-2025-08-07")
    print("Resposta RAG:\n", resposta)
    
'''TESTE COM TXT'''
if __name__ == "__main__":
    rag = RAGService()
    rag.carregar_documento('app\\documents\\GTB_gold_Nov23.txt')  # ajuste o caminho
    resposta = rag.rag("Resuma o conteúdo do documento.", model="gpt-5-nano-2025-08-07")
    print("Resposta RAG:\n", resposta)
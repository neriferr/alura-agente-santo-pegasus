"""
debug_retrieval.py
Script de diagnóstico: muestra exactamente qué fragmentos del documento
recupera el retriever para una pregunta dada, SIN pasar por Claude.
Sirve para detectar si el problema es de recuperación (retrieval) o
de generación (el LLM no usa bien el contexto).

Uso:
    python debug_retrieval.py "tu pregunta aquí"
"""

import sys
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def main():
    pregunta = sys.argv[1] if len(sys.argv) > 1 else "¿Qué herramientas se usan en el entorno de backend?"

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True
    )

    print(f"\nPregunta: {pregunta}\n")
    print("=" * 80)

    resultados = vectorstore.similarity_search_with_score(pregunta, k=8)

    for i, (doc, score) in enumerate(resultados, start=1):
        fuente = doc.metadata.get("source", "desconocido")
        pagina = doc.metadata.get("page", "?")
        print(f"\n--- Fragmento {i} | score={score:.4f} | fuente={fuente} | pagina={pagina} ---")
        print(doc.page_content[:400])
        print("...")


if __name__ == "__main__":
    main()

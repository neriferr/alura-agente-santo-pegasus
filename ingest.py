"""
ingest.py
Lee el/los PDF(s) de la carpeta docs/, los divide en chunks,
genera embeddings (locales, gratis, sin API key) y los guarda
en una base vectorial Chroma persistente en disco (vectorstore/).

Ejecutar UNA vez (o cada vez que cambien los documentos):
    python ingest.py
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DOCS_DIR = "docs"
VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def cargar_documentos():
    """Carga todos los PDFs de la carpeta docs/."""
    documentos = []
    if not os.path.isdir(DOCS_DIR):
        raise FileNotFoundError(
            f"No existe la carpeta '{DOCS_DIR}/'. Crea la carpeta y coloca "
            f"ahí tu(s) PDF(s) antes de correr este script."
        )

    archivos_pdf = [f for f in os.listdir(DOCS_DIR) if f.lower().endswith(".pdf")]
    if not archivos_pdf:
        raise FileNotFoundError(
            f"No se encontraron archivos .pdf dentro de '{DOCS_DIR}/'."
        )

    for nombre_archivo in archivos_pdf:
        ruta = os.path.join(DOCS_DIR, nombre_archivo)
        print(f"Cargando: {ruta}")
        loader = PyPDFLoader(ruta)
        documentos.extend(loader.load())

    return documentos


def dividir_en_chunks(documentos):
    """Divide los documentos en fragmentos manejables para el RAG."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=250,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documentos)
    print(f"Documentos divididos en {len(chunks)} chunks.")
    return chunks


def construir_vectorstore(chunks):
    """Genera embeddings y persiste la base vectorial (FAISS) en disco."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTORSTORE_DIR)
    print(f"Vectorstore creado y guardado en '{VECTORSTORE_DIR}/'.")
    return vectorstore


if __name__ == "__main__":
    docs = cargar_documentos()
    chunks = dividir_en_chunks(docs)
    construir_vectorstore(chunks)
    print("\n[OK] Ingesta completada. Ya puedes correr la app con: streamlit run app.py")

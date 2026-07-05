"""
rag_chain.py
Construye la cadena RAG: recupera los fragmentos más relevantes del
vectorstore y se los pasa a Claude junto con la pregunta del usuario
para generar una respuesta basada únicamente en el documento.
"""

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

PROMPT_TEMPLATE = """Eres el Alura Agente de Santo Pegasus Soluciones, un asistente
interno que responde preguntas de nuevos desarrolladores basándote
EXCLUSIVAMENTE en el contenido del manual de onboarding proporcionado.

Reglas:
- Responde siempre en español, de forma clara y directa.
- Si la respuesta no está en el contexto proporcionado, dilo explícitamente
  ("No encuentro esa información en el documento") en vez de inventar datos.
- Cuando sea posible, cita la sección o el tema del manual del que proviene
  la respuesta.

Contexto extraído del documento:
{context}

Pregunta del usuario:
{question}

Respuesta:"""


def formatear_contexto(documentos):
    return "\n\n---\n\n".join(doc.page_content for doc in documentos)


def cargar_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embeddings,
    )


def construir_cadena_rag():
    """Devuelve una cadena lista para invocar con .invoke('pregunta')."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise EnvironmentError(
            "No se encontró la variable de entorno ANTHROPIC_API_KEY. "
            "Definila antes de correr la app (ver README)."
        )

    vectorstore = cargar_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatAnthropic(
        model="claude-sonnet-5",
        temperature=0,
        max_tokens=1000,
    )

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    cadena = (
        {
            "context": retriever | formatear_contexto,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return cadena


if __name__ == "__main__":
    # Prueba rápida por consola
    cadena = construir_cadena_rag()
    print("Alura Agente listo. Escribe 'salir' para terminar.\n")
    while True:
        pregunta = input("Pregunta: ")
        if pregunta.lower() in ("salir", "exit", "quit"):
            break
        respuesta = cadena.invoke(pregunta)
        print(f"\nRespuesta: {respuesta}\n")

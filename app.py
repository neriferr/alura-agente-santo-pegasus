"""
app.py
Interfaz web (Streamlit) del Alura Agente para Santo Pegasus Soluciones.

Correr localmente:
    streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from rag_chain import construir_cadena_rag

load_dotenv()  # Carga ANTHROPIC_API_KEY desde un archivo .env si existe

st.set_page_config(page_title="Alura Agente | Santo Pegasus", page_icon="🤖")

st.title("🤖 Alura Agente — Santo Pegasus Soluciones")
st.caption(
    "Pregúntame sobre el Manual de Onboarding para Nuevos Desarrolladores "
    "(procesos, herramientas, arquitectura, buenas prácticas, etc.)"
)

# --- Validación de API Key ---
if not os.environ.get("ANTHROPIC_API_KEY"):
    st.error(
        "⚠️ No se encontró la variable de entorno ANTHROPIC_API_KEY. "
        "Configúrala antes de usar la app (ver README)."
    )
    st.stop()

# --- Cargar la cadena RAG una sola vez (cache) ---
@st.cache_resource(show_spinner="Cargando el agente...")
def obtener_cadena():
    return construir_cadena_rag()

cadena = obtener_cadena()

# --- Historial de conversación ---
if "historial" not in st.session_state:
    st.session_state.historial = []

for pregunta, respuesta in st.session_state.historial:
    with st.chat_message("user"):
        st.write(pregunta)
    with st.chat_message("assistant"):
        st.write(respuesta)

pregunta_usuario = st.chat_input("Escribe tu pregunta aquí...")

if pregunta_usuario:
    with st.chat_message("user"):
        st.write(pregunta_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en el manual..."):
            respuesta = cadena.invoke(pregunta_usuario)
        st.write(respuesta)

    st.session_state.historial.append((pregunta_usuario, respuesta))

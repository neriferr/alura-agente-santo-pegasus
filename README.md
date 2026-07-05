# 🤖 Alura Agente — Santo Pegasus Soluciones

Agente de inteligencia artificial (RAG) que responde preguntas sobre el
**Manual de Onboarding para Nuevos Desarrolladores** de Santo Pegasus
Soluciones, empresa ficticia especializada en microservicios e IA (RAG).

Proyecto desarrollado como Challenge Final del programa **ONE (Oracle
Next Education) - Alura**.

## 📌 Descripción del proyecto

Cualquier persona colaboradora puede hacerle preguntas en lenguaje natural
al agente (por ejemplo, sobre procesos de onboarding, herramientas usadas,
arquitectura de microservicios, protocolos internos, etc.) y recibir una
respuesta clara, generada a partir del contenido real del manual, sin
necesidad de abrir el PDF.

## 🏗️ Arquitectura de la solución

```
PDF (Manual de Onboarding)
        │
        ▼
  PyPDFLoader (lectura del PDF)
        │
        ▼
  RecursiveCharacterTextSplitter (división en chunks)
        │
        ▼
  HuggingFace Embeddings (all-MiniLM-L6-v2, local y gratuito)
        │
        ▼
  ChromaDB (base de datos vectorial persistente)
        │
        ▼
  Retriever (búsqueda semántica de los fragmentos más relevantes)
        │
        ▼
  Claude (Anthropic) vía LangChain → genera la respuesta final
        │
        ▼
  Interfaz Streamlit (chat web)
```

**Flujo (RAG - Retrieval Augmented Generation):**
1. El documento se procesa una única vez (`ingest.py`) y se convierte en
   una base vectorial.
2. Cuando el usuario hace una pregunta, se buscan los fragmentos del
   documento más relacionados semánticamente.
3. Esos fragmentos se envían a Claude junto con la pregunta, para que
   genere una respuesta basada solo en esa información.

## 🛠️ Tecnologías utilizadas

- **Python 3.11**
- **LangChain** — orquestación del pipeline RAG
- **Claude (Anthropic API)** — modelo de lenguaje (`claude-sonnet-5`)
- **PyPDF** — lectura del documento PDF
- **HuggingFace Sentence-Transformers** — generación de embeddings (local)
- **ChromaDB** — base de datos vectorial
- **Streamlit** — interfaz web del agente
- **Oracle Cloud Infrastructure (OCI Compute)** — despliegue en la nube

## 📂 Estructura del repositorio

```
santo-pegasus-rag-agent/
├── docs/                   # PDF(s) fuente (documento de la empresa)
├── vectorstore/            # Base vectorial generada (no se sube a git)
├── ingest.py               # Script de lectura y procesamiento del documento
├── rag_chain.py            # Pipeline RAG (retriever + prompt + Claude)
├── app.py                  # Interfaz Streamlit
├── requirements.txt        # Dependencias del proyecto
├── .env.example            # Plantilla de variables de entorno
└── README.md
```

## ▶️ Instrucciones para ejecutar el proyecto localmente

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/santo-pegasus-rag-agent.git
   cd santo-pegasus-rag-agent
   ```

2. Crear un entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar la clave de API:
   ```bash
   cp .env.example .env
   # Editar .env y colocar tu ANTHROPIC_API_KEY real
   ```

4. Colocar el PDF del manual dentro de la carpeta `docs/`.

5. Generar la base vectorial (solo la primera vez o si cambia el documento):
   ```bash
   python ingest.py
   ```

6. Ejecutar la aplicación:
   ```bash
   streamlit run app.py
   ```

7. Abrir el navegador en `http://localhost:8501`.

## 💬 Ejemplos de preguntas que el agente puede responder

- "¿Cuáles son los pasos del proceso de onboarding para un nuevo desarrollador?"
- "¿Qué herramientas se usan en el equipo de backend?"
- "¿Cuál es el protocolo a seguir ante un incidente de producción?"
- "¿Qué se espera de mí durante mi primera semana en la empresa?"

## 🗨️ Ejemplos de respuestas generadas por el agente

> _(Se completará con capturas reales una vez probado el agente)_

## ☁️ Despliegue en Oracle Cloud (OCI)

> _(Se completará con el enlace público y/o captura de pantalla una vez
> realizado el deploy)_

## 👤 Autor

Proyecto desarrollado por Neri como parte del Challenge Final del
programa ONE - Alura.

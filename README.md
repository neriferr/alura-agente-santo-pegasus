---
title: Alura Agente Santo Pegasus
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.40.1
app_file: app.py
pinned: false
---

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
PDF(s) (Manual de Onboarding + Guías de Ingeniería + Arquitectura + Incidentes)
        │
        ▼
  PyPDFLoader (lectura de todos los PDFs en docs/)
        │
        ▼
  RecursiveCharacterTextSplitter (división en chunks de ~1500 caracteres)
        │
        ▼
  HuggingFace Embeddings multilingües (paraphrase-multilingual-mpnet-base-v2)
        │
        ▼
  FAISS (base de datos vectorial persistente, local)
        │
        ▼
  Retriever (búsqueda semántica de los 10 fragmentos más relevantes)
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
- **HuggingFace Sentence-Transformers** — embeddings multilingües locales (`paraphrase-multilingual-mpnet-base-v2`)
- **FAISS** — base de datos vectorial (local, sin dependencias de compilación)
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
- "¿Qué debo hacer durante mi primera semana según el checklist de onboarding?"
- "¿Qué es el programa de buddy y cuánto dura?"
- "¿Qué herramientas se usan en el entorno de backend?"

## 🗨️ Ejemplos de respuestas generadas por el agente

**Pregunta:** ¿Qué debo hacer durante mi primera semana según el checklist de onboarding?

> Según la Sección 12 — Checklist de Onboarding — Semana 1, este checklist debe ser completado conjuntamente por vos (el nuevo desarrollador) y tu Tech Lead antes de finalizar la primera semana, y debe guardarse en Confluence en tu página personal de onboarding. Dentro del apartado 12.1 Accesos y Cuentas, el documento menciona específicamente estos ítems a verificar: correo corporativo (@santopegasus.com) funcionando, Slack instalado con los canales obligatorios unidos, y acceso a GitHub (organización privada) confirmado. Como contexto adicional, el objetivo de esta primera semana es tener el entorno configurado y conocer al equipo, no ser plenamente productivo — eso se espera recién alrededor del mes 3.

**Pregunta:** ¿Qué es el programa de buddy y cuánto dura?

> El buddy es un desarrollador Senior o Pleno que te acompaña durante tus primeros 30 días en Santo Pegasus Soluciones. Su rol es asegurarse de que no estés solo en tu proceso de integración, brindándote apoyo y guía mientras te adaptas al equipo y al flujo de trabajo.

**Pregunta:** ¿Qué herramientas se usan en el entorno de backend?

> Según el documento, el entorno de Back-end utiliza Java 17+, Spring Boot 3+, Spring Security y Spring Data JPA. Además, el stack tecnológico relacionado incluye: bases de datos (PostgreSQL, MongoDB, Redis), bases vectoriales (Pinecone, Qdrant), infraestructura cloud en AWS (RDS, SES, SQS, Secrets Manager, EC2/ECS), contenedorización (Docker, Docker Compose), CI/CD (GitHub Actions), observabilidad (SLF4J/Logback, Prometheus, Datadog), calidad de código (SonarQube, JUnit 5, Mockito, Testcontainers) y control de versiones (Git, GitFlow, Conventional Commits).

## ☁️ Despliegue en Oracle Cloud (OCI)

> _(Se completará con el enlace público y/o captura de pantalla una vez
> realizado el deploy)_

## 👤 Autor

Proyecto desarrollado por Neri como parte del Challenge Final del
programa ONE - Alura.

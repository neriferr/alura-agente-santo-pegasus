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

Agente de inteligencia artificial (RAG) que responde preguntas sobre 5 documentos
internos de **Santo Pegasus Soluciones**, empresa ficticia especializada en
microservicios e IA (RAG): el Manual de Onboarding, las Guías Oficiales de Ingeniería
Back-end y Front-end, el Protocolo de Respuesta a Incidentes y Post-Mortems, y el
documento de Arquitectura de Microservicios y Mapa de Dominios.

Proyecto desarrollado como Challenge Final del programa **ONE (Oracle
Next Education) - Alura**.

## 📌 Descripción del proyecto

Cualquier persona colaboradora puede hacerle preguntas en lenguaje natural
al agente (por ejemplo, sobre procesos de onboarding, herramientas usadas,
arquitectura de microservicios, protocolos internos, etc.) y recibir una
respuesta clara, generada a partir del contenido real de los documentos, sin
necesidad de abrirlos manualmente.

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
  HuggingFace Embeddings multilingües (paraphrase-multilingual-MiniLM-L12-v2)
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

- **Python 3.12**
- **LangChain** — orquestación del pipeline RAG
- **Claude (Anthropic API)** — modelo de lenguaje (`claude-sonnet-5`)
- **PyPDF** — lectura de los documentos PDF
- **HuggingFace Sentence-Transformers** — embeddings multilingües locales (`paraphrase-multilingual-MiniLM-L12-v2`)
- **PyTorch (CPU-only)** — backend de inferencia para los embeddings, instalado explícitamente
  en su variante liviana (`--extra-index-url https://download.pytorch.org/whl/cpu`) para
  reducir el consumo de memoria en el deploy
- **FAISS** — base de datos vectorial (local, sin dependencias de compilación)
- **Streamlit** — interfaz web del agente
- **Git LFS** — almacenamiento de archivos binarios pesados del repositorio (PDFs, índice
  vectorial, capturas)
- **Hugging Face Spaces** — despliegue en la nube

## 📂 Estructura del repositorio

```
alura-agente-santo-pegasus/
├── docs/                       # PDFs fuente de Santo Pegasus Soluciones (5 documentos)
├── vectorstore/                # Índice vectorial FAISS pre-generado (incluido en el repo)
├── ingest.py                   # Script de lectura y procesamiento de los documentos
├── rag_chain.py                # Pipeline RAG (retriever + prompt + Claude)
├── app.py                      # Interfaz Streamlit
├── requirements.txt            # Dependencias del proyecto
├── runtime.txt                 # Versión de Python fijada para plataformas de deploy
├── .env.example                # Plantilla de variables de entorno
├── .gitattributes               # Configuración de Git LFS (PDFs, índice vectorial, imágenes)
├── .gitignore
├── debug_retrieval.py           # Script de diagnóstico: inspecciona qué fragmentos recupera el retriever
├── check_pdfs.py                # Script de diagnóstico: verifica extracción de texto de cada PDF
├── grep_pdf.py                  # Script de diagnóstico: exporta el texto crudo de un PDF a .txt
└── README.md
```

> **Nota sobre Git LFS**: este repositorio usa [Git LFS](https://git-lfs.com/) para
> almacenar los PDFs, el índice vectorial (`vectorstore/`) y las imágenes. Si vas a
> clonar el repositorio, instala Git LFS primero (`git lfs install`) para que estos
> archivos se descarguen completos en vez de quedar como punteros vacíos.

## ▶️ Instrucciones para ejecutar el proyecto localmente

1. Clonar el repositorio (requiere [Git LFS](https://git-lfs.com/) instalado):
   ```bash
   git lfs install
   git clone https://github.com/neriferr/alura-agente-santo-pegasus.git
   cd alura-agente-santo-pegasus
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

4. Los 5 documentos PDF de Santo Pegasus Soluciones ya vienen incluidos en `docs/`, y el
   índice vectorial ya generado en `vectorstore/` — no es necesario ningún paso adicional
   para tenerlos disponibles.

5. (Opcional) Si agregas o cambias documentos en `docs/`, regenera el índice vectorial:
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

> Según la sección 1.5 "Ecosistema Tecnológico Principal" del manual, el ecosistema tecnológico estandarizado para el backend en Santo Pegasus Soluciones incluye: Lenguaje & Runtime — Java 17+ (LTS), con adopción gradual de Java 21 (Virtual Threads); Framework Principal — Spring Boot 3+, Spring Security, Spring Cloud; Contenedorización — Docker (imágenes inmutables), orquestadas en AWS ECS Fargate; Bases de Datos — PostgreSQL (relacional), MongoDB/AWS DocumentDB (documentos), Redis/AWS ElastiCache (caché); Mensajería — AWS SQS; Autenticación — JWT + OAuth 2.0/OpenID Connect. Adicionalmente, en observabilidad se usan SLF4J/Logback, Spring Boot Actuator, Micrometer y Prometheus, y en infraestructura se usa Terraform/AWS CDK (Infrastructure as Code) y Flyway/Liquibase para migraciones de base de datos.

## ☁️ Despliegue en la nube

La aplicación está desplegada públicamente en **Hugging Face Spaces**:

🔗 **https://neriferr26-alura-agente-santo-pegasus.hf.space/**

Repositorio del Space: https://huggingface.co/spaces/neriferr26/alura-agente-santo-pegasus

> Nota: se optó por Hugging Face Spaces en lugar de OCI Compute (sugerencia original del
> challenge) por ser una alternativa gratuita, mejor adaptada a aplicaciones con modelos
> de embeddings (más memoria disponible en su tier gratuito), y con deploy directo desde
> Git. El challenge permite explícitamente usar la herramienta que mejor se ajuste al
> proyecto.

## 👤 Autor

Proyecto desarrollado por Neri como parte del Challenge Final del
programa ONE - Alura.

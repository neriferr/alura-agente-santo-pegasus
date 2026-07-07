"""
check_pdfs.py
Verifica, PDF por PDF dentro de docs/, cuántas paginas tiene y cuanto
texto se logro extraer de cada una. Sirve para detectar PDFs escaneados
(imagenes) o con extraccion de texto defectuosa.

Uso:
    python check_pdfs.py
"""

import os
from pypdf import PdfReader

DOCS_DIR = "docs"

for nombre in os.listdir(DOCS_DIR):
    if not nombre.lower().endswith(".pdf"):
        continue

    ruta = os.path.join(DOCS_DIR, nombre)
    reader = PdfReader(ruta)
    total_chars = 0
    paginas_vacias = 0

    for pagina in reader.pages:
        texto = pagina.extract_text() or ""
        total_chars += len(texto.strip())
        if len(texto.strip()) < 20:
            paginas_vacias += 1

    print(f"\nArchivo: {nombre}")
    print(f"  Paginas: {len(reader.pages)}")
    print(f"  Caracteres totales extraidos: {total_chars}")
    print(f"  Paginas casi vacias (<20 caracteres): {paginas_vacias}")

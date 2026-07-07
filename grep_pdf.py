"""
grep_pdf.py
Busca palabras clave dentro del texto extraido de un PDF especifico,
para ver el vocabulario real que usa el documento (util para ajustar
las preguntas de prueba o el chunking).

Uso:
    python grep_pdf.py "docs/Santo Pegasus Soluciones Gu\u00eda Oficial de Ingenier\u00eda Back-end.pdf"
"""

import sys
from pypdf import PdfReader

ruta = sys.argv[1]
reader = PdfReader(ruta)

texto_completo = ""
for i, pagina in enumerate(reader.pages):
    texto_completo += f"\n\n===== PAGINA {i + 1} =====\n\n"
    texto_completo += pagina.extract_text() or ""

# Guardamos todo el texto extraido en un .txt para poder leerlo comodo
salida = "backend_guide_extraido.txt"
with open(salida, "w", encoding="utf-8") as f:
    f.write(texto_completo)

print(f"Texto completo extraido guardado en: {salida}")
print(f"Total de caracteres: {len(texto_completo)}")

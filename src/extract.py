# Extracts raw text from .pdf files
import pymupdf
import os
import json

def extract_page_text(page):
    blocks = page.get_text("blocks")
    page_width = page.rect.width
    mid_x = page_width/2

    left_col = []
    right_col = []

    for b in blocks:
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4]
        block_width = x1 - x0
        # treat wide blocks (titles, full-width figures/captions) as spanning both columns
        if block_width > page_width * 0.6:
            left_col.append((y0, text)) # flush as its own line, in position order
        elif x0 < mid_x:
            left_col.append((y0, text))
        else:
            right_col.append((y0, text))

    left_col.sort(key=lambda t: t[0])
    right_col.sort(key=lambda t: t[0])

    return "".join(t[1] for t in left_col) + "".join(t[1] for t in right_col)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
pdf_dir = os.path.join(PROJECT_ROOT, "data", "papers")
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
extracted = {}

for filename in pdf_files:
    doc = pymupdf.open(os.path.join(pdf_dir, filename))
    full_text = ""
    for page in doc:
        full_text += extract_page_text(page)
    extracted[filename] =full_text
    doc.close()
output_path = os.path.join(PROJECT_ROOT, "data", "extracted_text.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(extracted, f, ensure_ascii=False, indent=2)
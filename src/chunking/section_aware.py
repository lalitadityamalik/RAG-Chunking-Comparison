import pymupdf
import os
def extract_page_span(page):
    result = []
    page_dict = page.get_text("dict")
    for block in page_dict["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                text = span["text"]
                size = span["size"]
                flags = span["flags"]
                result.append([text, size, flags])
    return result
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
pdf_dir = os.path.join(PROJECT_DIR, "data", "papers")

if __name__ == "__main__":
    doc = pymupdf.open(os.path.join(pdf_dir, "2606.30774v1.pdf"))
    page = doc[0]
    for text,size,flags in extract_page_span(page):
        print(text[:50], size, flags)

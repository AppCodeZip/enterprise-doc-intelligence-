from pypdf import PdfReader
from docx import Document
import os

def load_pdf(file_path):
    reader = PdfReader(file_path)
    pages = []
    for i, page in enumerate(reader.pages):
        pages.append({
            "text": page.extract_text(),
            "metadata": {
                "source": os.path.basename(file_path),
                "page": i + 1
            }
        })
    return pages

def load_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return [{
        "text": text,
        "metadata": {
            "source": os.path.basename(file_path),
            "page": 1
        }
    }]

def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return [{
        "text": text,
        "metadata": {
            "source": os.path.basename(file_path),
            "page": 1
        }
    }]

def load_document(file_path):
    print("Starting loaders script...")
    if file_path.endswith(".pdf"):
        return load_pdf(file_path)
    elif file_path.endswith(".docx"):
        return load_docx(file_path)
    elif file_path.endswith(".txt") or file_path.endswith(".md"):
        return load_txt(file_path)
    else:
        raise ValueError("Unsupported file format")

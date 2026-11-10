
from pathlib import Path
import fitz
from docx import Document


def extract_pdf_text(file_path):
    extracted_pages = []

    with fitz.open(file_path) as pdf:
        for page in pdf:
            extracted_pages.append(page.get_text("text"))

    return "\n".join(extracted_pages).strip()


def extract_docx_text(file_path):
    document = Document(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()


def extract_document_text(file_path, file_type):
    if file_type == "pdf":
        return extract_pdf_text(file_path)

    if file_type == "docx":
        return extract_docx_text(file_path)

    raise ValueError("Unsupported document format.")

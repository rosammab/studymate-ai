
from pathlib import Path

import pymupdf
from docx import Document


MAX_EXTRACTED_TEXT_LENGTH = 2_000_000


def extract_pdf_text(file_path):

    extracted_pages = []

    try:
        with pymupdf.open(file_path) as pdf:

            if pdf.is_encrypted:
                raise ValueError(
                    "Password-protected PDFs are not supported."
                )

            for page in pdf:
                extracted_pages.append(
                    page.get_text("text")
                )

    except Exception as error:
        raise ValueError(
            f"Unable to read PDF file: {error}"
        )

    return "\n".join(extracted_pages).strip()


def extract_docx_text(file_path):

    try:
        document = Document(file_path)

        extracted_content = []

        # Extract paragraphs
        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                extracted_content.append(text)

        # Extract table contents
        for table in document.tables:
            for row in table.rows:
                row_text = [
                    cell.text.strip()
                    for cell in row.cells
                    if cell.text.strip()
                ]

                if row_text:
                    extracted_content.append(
                        " | ".join(row_text)
                    )

    except Exception as error:
        raise ValueError(
            f"Unable to read DOCX file: {error}"
        )

    return "\n".join(extracted_content).strip()


def extract_document_text(file_path, file_type):

    if file_type == "pdf":
        extracted_text = extract_pdf_text(file_path)

    elif file_type == "docx":
        extracted_text = extract_docx_text(file_path)

    else:
        raise ValueError(
            "Unsupported document format."
        )

    if not extracted_text:
        raise ValueError(
            "No readable text found. Scanned PDFs may require OCR."
        )

    if len(extracted_text) > MAX_EXTRACTED_TEXT_LENGTH:
        raise ValueError(
            "Extracted document text exceeds the allowed limit."
        )

    return extracted_text

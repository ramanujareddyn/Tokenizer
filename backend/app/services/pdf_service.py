from __future__ import annotations

import fitz

from app.core.exceptions import PDFExtractionError


class PDFService:
    @staticmethod
    def extract_text(file_bytes: bytes) -> str:
        try:
            with fitz.open(stream=file_bytes, filetype="pdf") as document:
                text_parts: list[str] = []
                for page in document:
                    page_text = page.get_text("text")
                    if page_text and page_text.strip():
                        text_parts.append(page_text)
                extracted_text = "\n".join(text_parts).strip()
                if not extracted_text:
                    raise PDFExtractionError("No text could be extracted from the PDF.")
                return extracted_text
        except Exception as exc:
            raise PDFExtractionError("Unable to read the uploaded PDF.") from exc

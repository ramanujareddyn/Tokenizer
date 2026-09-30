import os
from typing import Any

import tiktoken


class FileService:
    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
    ALLOWED_TEXT_EXTENSIONS = {".txt"}
    ALLOWED_PDF_EXTENSION = ".pdf"

    def validate_text_input(self, text: str | None) -> str:
        if text is None or text.strip() == "":
            raise ValueError("empty input")
        return text.strip()

    def validate_tiktoken_encoding(self, encoding: str | None) -> str:
        if not encoding:
            raise ValueError("unsupported encoding")
        try:
            tiktoken.get_encoding(encoding)
            return encoding
        except Exception as exc:
            raise ValueError(f"unsupported encoding: {encoding}") from exc

    def validate_file_upload(self, filename: str | None, file_size: int | None) -> None:
        if not filename:
            raise ValueError("empty file name")

        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.ALLOWED_TEXT_EXTENSIONS | {self.ALLOWED_PDF_EXTENSION}:
            raise ValueError("unsupported file type")

        if file_size is None:
            raise ValueError("file size unavailable")

        if file_size > self.MAX_FILE_SIZE_BYTES:
            raise ValueError("file too large")

    def validate_pdf_bytes(self, file_bytes: bytes | None) -> bytes:
        if not file_bytes:
            raise ValueError("empty pdf content")
        if len(file_bytes) > self.MAX_FILE_SIZE_BYTES:
            raise ValueError("file too large")
        return file_bytes

    def normalize_text(self, text: str) -> str:
        return text.replace("\r\n", "\n").replace("\r", "\n")

    def get_source_type(self, filename: str | None, explicit_source: str | None = None) -> str:
        if explicit_source:
            return explicit_source
        if not filename:
            return "text"
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".txt":
            return "txt"
        if ext == ".pdf":
            return "pdf"
        return "text"

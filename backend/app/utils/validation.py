from __future__ import annotations

import os

import tiktoken

from app.core.config import settings


def validate_text_input(text: str | None) -> str:
    if text is None or text.strip() == "":
        raise ValueError("empty input")
    return text.strip()


def validate_tiktoken_encoding(encoding: str | None) -> str:
    if not encoding:
        raise ValueError("unsupported encoding")
    try:
        tiktoken.get_encoding(encoding)
        return encoding
    except Exception as exc:  # pragma: no cover - wrapped for consistent API handling
        raise ValueError(f"unsupported encoding: {encoding}") from exc


def validate_upload(filename: str | None, file_size: int | None) -> None:
    if not filename:
        raise ValueError("empty file name")

    extension = os.path.splitext(filename)[1].lower()
    if extension not in {".txt", ".pdf"}:
        raise ValueError("unsupported file type")

    if file_size is None:
        raise ValueError("file size unavailable")

    if file_size > settings.max_upload_size_bytes:
        raise ValueError("file too large")

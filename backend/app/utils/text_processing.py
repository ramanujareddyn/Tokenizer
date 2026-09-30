from __future__ import annotations


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def get_source_type(filename: str | None) -> str:
    if not filename:
        return "text"
    extension = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if extension == "txt":
        return "txt"
    if extension == "pdf":
        return "pdf"
    return "text"

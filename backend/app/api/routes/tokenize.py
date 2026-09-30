from __future__ import annotations

from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.services.custom_tokenizer_service import CustomTokenizerService
from app.services.file_service import FileService
from app.services.pdf_service import PDFService
from app.services.stats_service import StatsService
from app.services.tiktoken_service import TiktokenService
from app.utils.text_processing import normalize_text
from app.utils.validation import validate_text_input, validate_tiktoken_encoding, validate_upload

router = APIRouter(tags=["tokenizer"])
file_service = FileService()
custom_tokenizer = CustomTokenizerService(initial_vocab=settings.custom_vocabulary_baseline.copy())


@router.post("/tokenize")
async def tokenize_text(payload: dict[str, Any]) -> dict[str, Any]:
    text = payload.get("text")
    mode = payload.get("mode", "tiktoken")
    encoding = payload.get("encoding", settings.default_encoding)
    try:
        normalized_text = validate_text_input(text)
        normalized_text = normalize_text(normalized_text)
        if mode == "tiktoken":
            validate_tiktoken_encoding(encoding)
            result = TiktokenService().tokenize(normalized_text, encoding)
        elif mode == "custom":
            custom_result = custom_tokenizer.tokenize(normalized_text)
            result = {
                "token_ids": custom_result["token_ids"],
                "decoded_tokens": custom_result["decoded_tokens"],
                "token_count": custom_result["token_count"],
                "selected_encoding": None,
                "selected_mode": "custom",
                "vocabulary": custom_result["vocabulary"],
                "newly_created_tokens": custom_result["newly_created_tokens"],
            }
        else:
            raise ValueError("unsupported mode")

        result["selected_mode"] = mode
        result["statistics"] = StatsService.compute(normalized_text, result["token_count"])
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/process-file")
async def process_file(file: UploadFile = File(...)) -> dict[str, Any]:
    try:
        file_bytes = await file.read()
        validate_upload(file.filename, len(file_bytes))
        if file.filename.lower().endswith(".pdf"):
            extracted_text = PDFService.extract_text(file_bytes)
            return {
                "filename": file.filename,
                "source_type": "pdf",
                "text": extracted_text,
                "stats": StatsService.compute(extracted_text, len(extracted_text.split() or [])),
            }
        text = file_bytes.decode("utf-8")
        normalized_text = normalize_text(validate_text_input(text))
        return {
            "filename": file.filename,
            "source_type": "txt",
            "text": normalized_text,
            "stats": StatsService.compute(normalized_text, len(normalized_text.split() or [])),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/reset-vocabulary")
async def reset_vocabulary() -> dict[str, Any]:
    custom_tokenizer.reset()
    custom_tokenizer._vocabulary.update(settings.custom_vocabulary_baseline.copy())
    for token, token_id in settings.custom_vocabulary_baseline.items():
        custom_tokenizer._frequency[token] = 0
    return {"status": "reset", "baseline": settings.custom_vocabulary_baseline.copy()}

from __future__ import annotations

from pydantic import BaseModel, Field


class TokenizeRequest(BaseModel):
    text: str
    mode: str = "tiktoken"
    encoding: str = "gpt2"
    custom_vocabulary: dict[str, int] | None = None


class TokenizeResponse(BaseModel):
    token_ids: list[int]
    decoded_tokens: list[str]
    token_count: int
    selected_mode: str
    selected_encoding: str | None = None
    vocabulary: dict[int, dict] | None = None
    newly_created_tokens: list[str] | None = None
    statistics: dict


class FileTokenizeRequest(BaseModel):
    text: str = Field(..., min_length=1)
    mode: str = "tiktoken"
    encoding: str = "gpt2"


class ErrorResponse(BaseModel):
    detail: str

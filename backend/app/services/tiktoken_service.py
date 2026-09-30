from __future__ import annotations

import tiktoken


class TiktokenService:
    def tokenize(self, text: str, encoding: str) -> dict:
        valid_encoding = self.validate_encoding(encoding)
        token_ids = tiktoken.get_encoding(valid_encoding).encode(text)
        decoded_tokens = [tiktoken.get_encoding(valid_encoding).decode([token_id]) for token_id in token_ids]

        return {
            "token_ids": list(token_ids),
            "decoded_tokens": decoded_tokens,
            "token_count": len(token_ids),
            "selected_encoding": valid_encoding,
            "metadata": {"encoding": valid_encoding},
        }

    def validate_encoding(self, encoding: str | None) -> str:
        if not encoding:
            raise ValueError("unsupported encoding")
        try:
            tiktoken.get_encoding(encoding)
            return encoding
        except Exception as exc:
            raise ValueError(f"unsupported encoding: {encoding}") from exc

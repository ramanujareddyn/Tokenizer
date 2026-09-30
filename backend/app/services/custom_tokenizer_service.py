import re
from collections import defaultdict


class CustomTokenizerService:
    def __init__(self, initial_vocab: dict[str, int] | None = None):
        self._vocabulary = dict(initial_vocab or {})
        self._frequency = defaultdict(int)
        for token, token_id in (initial_vocab or {}).items():
            self._frequency[token] = 0

    def tokenize(self, text: str) -> dict:
        tokens = re.findall(r"\S+", text)
        token_ids: list[int] = []
        decoded_tokens: list[str] = []
        new_tokens: list[str] = []
        seen_new_tokens: set[str] = set()

        for token in tokens:
            if token in self._vocabulary:
                token_id = self._vocabulary[token]
                self._frequency[token] += 1
            else:
                token_id = max(self._vocabulary.values(), default=0) + 1
                while token_id in self._vocabulary.values():
                    token_id += 1
                self._vocabulary[token] = token_id
                self._frequency[token] = 1
                if token not in seen_new_tokens:
                    new_tokens.append(token)
                    seen_new_tokens.add(token)
            token_ids.append(token_id)
            decoded_tokens.append(token)

        vocabulary_snapshot = {
            token_id: {
                "id": token_id,
                "token": token,
                "frequency": self._frequency.get(token, 0),
                "status": "new" if token in new_tokens else "existing",
            }
            for token, token_id in sorted(self._vocabulary.items(), key=lambda item: item[1])
        }

        return {
            "token_ids": token_ids,
            "decoded_tokens": decoded_tokens,
            "token_count": len(token_ids),
            "vocabulary": vocabulary_snapshot,
            "newly_created_tokens": new_tokens,
            "metadata": {"mode": "custom"},
        }

    def reset(self) -> None:
        self._vocabulary.clear()
        self._frequency.clear()

    def get_vocabulary_snapshot(self) -> dict[int, dict]:
        return {
            token_id: {
                "id": token_id,
                "token": token,
                "frequency": self._frequency.get(token, 0),
                "status": "existing",
            }
            for token, token_id in sorted(self._vocabulary.items(), key=lambda item: item[1])
        }

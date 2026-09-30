class StatsService:
    @staticmethod
    def compute(text: str, token_count: int) -> dict:
        char_count = len(text)
        word_count = len(text.split()) if text.strip() else 0
        tokens_per_word = (token_count / word_count) if word_count else 0.0
        tokens_per_character = (token_count / char_count) if char_count else 0.0

        return {
            "character_count": char_count,
            "word_count": word_count,
            "token_count": token_count,
            "tokens_per_word": round(tokens_per_word, 4),
            "tokens_per_character": round(tokens_per_character, 4),
        }

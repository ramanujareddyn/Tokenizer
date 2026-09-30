from app.services.tiktoken_service import TiktokenService


def test_tiktoken_service_returns_real_encoding_output():
    service = TiktokenService()

    result = service.tokenize("hello world", "gpt2")

    assert result["token_count"] > 0
    assert result["token_ids"]
    assert result["decoded_tokens"]
    assert result["selected_encoding"] == "gpt2"

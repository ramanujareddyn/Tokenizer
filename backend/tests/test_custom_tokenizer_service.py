from app.services.custom_tokenizer_service import CustomTokenizerService


def test_custom_tokenizer_reuses_existing_ids_and_tracks_new_tokens():
    service = CustomTokenizerService(initial_vocab={"hello": 1, "world": 2})

    result = service.tokenize("hello world hello alpha")

    assert result["token_ids"] == [1, 2, 1, 3]
    assert result["newly_created_tokens"] == ["alpha"]
    assert result["vocabulary"][3]["token"] == "alpha"
    assert result["vocabulary"][3]["frequency"] == 1
    assert result["vocabulary"][1]["frequency"] == 2

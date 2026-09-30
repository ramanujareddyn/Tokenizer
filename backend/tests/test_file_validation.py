import pytest

from app.services.file_service import FileService


@pytest.mark.parametrize(
    "input_text, expected_message",
    [
        ("", "empty"),
        (None, "empty"),
    ],
)
def test_validate_text_input_rejects_empty_input(input_text, expected_message):
    service = FileService()

    with pytest.raises(ValueError, match=expected_message):
        service.validate_text_input(input_text)


def test_validate_encoding_rejects_unsupported_encoding():
    service = FileService()

    with pytest.raises(ValueError, match="unsupported"):
        service.validate_tiktoken_encoding("not-a-real-encoding")

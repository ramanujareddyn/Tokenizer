class TokenizerError(Exception):
    """Base exception for tokenizer application errors."""


class ValidationError(TokenizerError):
    """Raised when client input fails validation."""


class PDFExtractionError(TokenizerError):
    """Raised when a PDF cannot be read or has no extractable text."""

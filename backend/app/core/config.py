from dataclasses import dataclass, field


@dataclass
class AppConfig:
    app_name: str = "TOkenizer"
    default_encoding: str = "gpt2"
    max_upload_size_bytes: int = 10 * 1024 * 1024
    custom_vocabulary_baseline: dict[str, int] = field(
        default_factory=lambda: {"hello": 1, "world": 2}
    )


settings = AppConfig()

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class KimiConfig:
    model: str = "kimi-k2.5"
    temperature: float = 0.3
    max_tokens: int = 4096


@dataclass(frozen=True)
class AppConfig:
    kimi: KimiConfig = KimiConfig()
    telegram_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    obsidian_vault: str = "/app/obsidian_hub"
    sandbox_path: str = "/app/sandbox"

# personal_agent/core/config.py
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class AppConfig:
    llm_provider: str
    llm_model: str
    llm_base_url: str
    llm_timeout: int
    llm_max_retries: int
    obsidian_vault_path: Path
    sandbox_path: Path
    quarantine_path: Path
    prompts_path: Path
    memory_lab_path: Path
    schedule_priority_default: int
    document_sync_interval_seconds: int
    event_bus_queue_max_size: int
    kimi_api_key: str
    openrouter_api_key: str
    telegram_bot_token: str


def load_config(config_path: Path | None = None, env_path: Path | None = None) -> AppConfig:
    root = Path(__file__).resolve().parent.parent
    cfg_path = config_path or root / "config.yaml"
    dotenv_path = env_path or root / ".env"

    raw = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

    env: dict[str, str] = {}
    if dotenv_path.exists():
        for line in dotenv_path.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()

    return AppConfig(
        llm_provider=raw["llm"]["provider"],
        llm_model=raw["llm"]["model"],
        llm_base_url=raw["llm"]["base_url"],
        llm_timeout=raw["llm"]["timeout"],
        llm_max_retries=raw["llm"]["max_retries"],
        obsidian_vault_path=Path(raw["paths"]["obsidian_vault"]),
        sandbox_path=Path(raw["paths"]["sandbox"]),
        quarantine_path=Path(raw["paths"]["quarantine"]),
        prompts_path=Path(raw["paths"]["prompts"]),
        memory_lab_path=Path(raw["paths"]["memory_lab"]),
        schedule_priority_default=raw["thresholds"]["schedule_priority_default"],
        document_sync_interval_seconds=raw["thresholds"]["document_sync_interval_seconds"],
        event_bus_queue_max_size=raw["event_bus"]["queue_max_size"],
        kimi_api_key=env.get("KIMI_API_KEY", ""),
        openrouter_api_key=env.get("OPENROUTER_API_KEY", ""),
        telegram_bot_token=env.get("TELEGRAM_BOT_TOKEN", ""),
    )

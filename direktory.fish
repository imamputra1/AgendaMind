#!/usr/bin/fish

# Gunakan variabel lokal agar tidak mengotori sesi shell
set -l BASE_DIR ~/prog_lang/python/personal_agent
mkdir -p $BASE_DIR
cd $BASE_DIR

echo "Membangun struktur direktori di $BASE_DIR..."

mkdir -p \
  core \
  interfaces/obsidian_hub \
  interfaces/telegram_node \
  interfaces/calendar_adapter \
  features/executive_secretary \
  features/document_controller \
  prompts \
  sandbox

# Buat file __init__.py secara massal
touch core/__init__.py \
      interfaces/__init__.py \
      interfaces/obsidian_hub/__init__.py \
      interfaces/telegram_node/__init__.py \
      interfaces/calendar_adapter/__init__.py \
      features/__init__.py \
      features/executive_secretary/__init__.py \
      features/document_controller/__init__.py

# Core: Config
printf "%s\n" \
  "from dataclasses import dataclass" \
  "" \
  "@dataclass(frozen=True)" \
  "class KimiConfig:" \
  '    model: str = "kimi-k2.5"' \
  "    temperature: float = 0.3" \
  "    max_tokens: int = 4096" \
  "" \
  "@dataclass(frozen=True)" \
  "class AppConfig:" \
  "    kimi: KimiConfig = KimiConfig()" \
  > core/config.py

# Core: Event Bus
printf "%s\n" \
  "from collections import defaultdict" \
  "from typing import Callable, Any" \
  "" \
  "class EventBus:" \
  "    def __init__(self) -> None:" \
  "        self._listeners: dict[str, list[Callable[..., Any]]] = defaultdict(list)" \
  "" \
  "    def subscribe(self, event_type: str, handler: Callable[..., Any]) -> None:" \
  "        self._listeners[event_type].append(handler)" \
  "" \
  "    def publish(self, event_type: str, payload: Any = None) -> None:" \
  "        for handler in self._listeners.get(event_type, []):" \
  "            handler(payload)" \
  > core/event_bus.py

# Interface: Obsidian
printf "%s\n" \
  "from core.event_bus import EventBus" \
  "" \
  "class ObsidianHub:" \
  '    """Captures filesystem signals from Obsidian vault and emits domain events."""' \
  "" \
  "    def __init__(self, bus: EventBus, vault_path: str) -> None:" \
  "        self.bus = bus" \
  "        self.vault_path = vault_path" \
  "" \
  "    def emit_note_created(self, note_path: str) -> None:" \
  '        self.bus.publish("note.created", {"path": note_path})' \
  > interfaces/obsidian_hub/reader.py

# Feature: Secretary
printf "%s\n" \
  "class ExecutiveSecretary:" \
  '    """Reacts to schedule and message events; handles prioritization logic."""' \
  "" \
  "    def handle_schedule_alert(self, payload: dict) -> None:" \
  '        print(f"[ExecutiveSecretary] Processing schedule: {payload}")' \
  "" \
  "    def handle_message_received(self, payload: dict) -> None:" \
  '        print(f"[ExecutiveSecretary] Processing message: {payload}")' \
  > features/executive_secretary/scheduler.py

# Prompts
printf "%s\n" \
  "# MATRIKS PRIORITAS JADWAL" \
  "" \
  "| Kode | Kategori              | Tindakan                              |" \
  "|------|----------------------|---------------------------------------|" \
  "| P1   | URGENT & IMPORTANT   | Eksekusi segera, notifikasi aktif.    |" \
  "| P2   | IMPORTANT NOT URGENT | Jadwalkan blok waktu fokus.           |" \
  "| P3   | URGENT NOT IMPORTANT | Delegasikan jika memungkinkan.        |" \
  "| P4   | NEITHER              | Tunda atau hapus.                     |" \
  "" \
  "Setiap jadwal baru WAJIB diberi tag [P1] s/d [P4]." \
  > prompts/prioritas_jadwal.md

# Main entry point (Template)
printf "%s\n" \
  "from core.config import AppConfig" \
  "from core.event_bus import EventBus" \
  'if __name__ == "__main__":' \
  "    print('Agent Core Initialized.')" \
  > main.py

echo "Struktur selesai dibuat!"
tree -L 3


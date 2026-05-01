from core.event_bus import EventBus

class ObsidianHub:
    """Captures filesystem signals from Obsidian vault and emits domain events."""

    def __init__(self, bus: EventBus, vault_path: str) -> None:
        self.bus = bus
        self.vault_path = vault_path

    def emit_note_created(self, note_path: str) -> None:
        self.bus.publish("note.created", {"path": note_path})

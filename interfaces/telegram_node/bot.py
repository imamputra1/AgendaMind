from typing import Any
from core.event_bus import EventBus


class TelegramNode:
    """Capture incoming Telegram messages and emits domain events."""

    def __init__(self, bus: EventBus, token: str) -> None:
        self.bus: EventBus = bus
        self.token: str = token
        
    def emit_message_received(self, text: str) -> None:
        self.bus.publish(\"message.received\", {\"text\": text})

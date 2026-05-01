from typing import Any
from core.event_bus import EventBus


class CalendarAdapter:
    """Bridges external calender alerts into internal domain events."""

    def __init__(self, bus: EventBus) -> None:
        self.bus: EventBus = bus

    def emit_schedule_alert(self, event_data: dict[str, Any]) -> None:
        self.bus.publish(\"schedule.alert\", event_data)

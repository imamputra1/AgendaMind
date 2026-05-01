from collections import defaultdict
from typing import Callable, Any

class EventBus:
    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable[..., Any]) -> None:
        self._listeners[event_type].append(handler)

    def publish(self, event_type: str, payload: Any = None) -> None:
        for handler in self._listeners.get(event_type, []):
            handler(payload)

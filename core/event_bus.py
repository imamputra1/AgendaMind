# personal_agent/core/event_bus.py
from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List

EventHandler = Callable[[Dict[str, Any]], Awaitable[None]]


@dataclass(frozen=True)
class Event:
    topic: str
    payload: Dict[str, Any]


class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[EventHandler]] = defaultdict(list)

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        self._subscribers[topic].append(handler)

    async def publish(self, event: Event) -> None:
        handlers = self._subscribers.get(event.topic, [])
        await asyncio.gather(*(h(event.payload) for h in handlers), return_exceptions=True)

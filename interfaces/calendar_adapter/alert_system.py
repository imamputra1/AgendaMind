# personal_agent/interfaces/calendar_adapter/alert_system.py
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Awaitable, Callable

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CalendarAlert:
    uid: str
    summary: str
    start_time: datetime
    end_time: datetime
    description: str = ""


AlertHandler = Callable[[CalendarAlert], Awaitable[None]]


class CalendarAlertSystem:
    def __init__(self, poll_interval_seconds: int = 60) -> None:
        self._poll_interval = poll_interval_seconds
        self._handlers: list[AlertHandler] = []
        self._task: asyncio.Task | None = None
        self._running = False

    def register_handler(self, handler: AlertHandler) -> None:
        self._handlers.append(handler)

    async def _poll(self) -> None:
        while self._running:
            alerts = await self._fetch_upcoming()
            for alert in alerts:
                await asyncio.gather(*(h(alert) for h in self._handlers), return_exceptions=True)
            await asyncio.sleep(self._poll_interval)

    async def _fetch_upcoming(self) -> list[CalendarAlert]:
        return []

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._poll())
        logger.info("Calendar alert system started")

    def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
        logger.info("Calendar alert system stopped")

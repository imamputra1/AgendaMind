# personal_agent/interfaces/telegram_node/webhook.py
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TelegramMessage:
    chat_id: int
    text: str
    username: str
    message_id: int


TelegramHandler = Callable[[TelegramMessage], Awaitable[None]]


class TelegramWebhookServer:
    def __init__(self, token: str, host: str = "0.0.0.0", port: int = 8080) -> None:
        self._token = token
        self._host = host
        self._port = port
        self._handlers: list[TelegramHandler] = []

    def register_handler(self, handler: TelegramHandler) -> None:
        self._handlers.append(handler)

    async def _dispatch(self, payload: dict[str, Any]) -> None:
        msg = self._parse(payload)
        if msg is None:
            return
        await asyncio.gather(*(h(msg) for h in self._handlers), return_exceptions=True)

    def _parse(self, payload: dict[str, Any]) -> TelegramMessage | None:
        try:
            message = payload["message"]
            return TelegramMessage(
                chat_id=message["chat"]["id"],
                text=message.get("text", ""),
                username=message["from"].get("username", "unknown"),
                message_id=message["message_id"],
            )
        except (KeyError, TypeError):
            logger.warning("Malformed Telegram payload: %s", payload)
            return None

    async def start(self) -> None:
        from aiohttp import web

        async def handle(request: web.Request) -> web.Response:
            payload = await request.json()
            await self._dispatch(payload)
            return web.Response(status=200)

        app = web.Application()
        app.router.add_post(f"/webhook/{self._token}", handle)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self._host, self._port)
        await site.start()
        logger.info("Telegram webhook listening on %s:%d", self._host, self._port)

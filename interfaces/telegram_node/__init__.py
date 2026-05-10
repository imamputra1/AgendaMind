# personal_agent/interfaces/telegram_node/__init__.py
from interfaces.telegram_node.webhook import TelegramMessage, TelegramWebhookServer

__all__ = ["TelegramMessage", "TelegramWebhookServer"]

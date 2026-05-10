# personal_agent/main.py
import asyncio

from core.config import load_config
from core.event_bus import EventBus


async def main() -> None:
    config = load_config()
    bus = EventBus()

    # TODO: compose agents and register listeners here

    print(f"Agent swarm initialized. LLM: {config.llm_model}")


if __name__ == "__main__":
    asyncio.run(main())

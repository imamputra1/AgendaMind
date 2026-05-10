FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    PATH="/app/.venv/bin:$PATH"

RUN groupadd --gid 1000 agentuser && \
    useradd --uid 1000 --gid agentuser --shell /bin/bash --create-home agentuser

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /usr/local/bin/uvx

WORKDIR /app

RUN mkdir -p /app/quarantine && \
    chown -R agentuser:agentuser /app

RUN uv pip install --system bandit

USER agentuser

CMD ["python"]

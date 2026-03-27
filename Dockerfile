FROM python:3.11-slim

WORKDIR /app

COPY uv.lock pyproject.toml .

COPY --from=ghcr.io/astral-sh/uv:0.10.2 /uv /uvx /bin/

ENV UV_NO_DEV=1

RUN uv sync --locked

COPY . .

CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

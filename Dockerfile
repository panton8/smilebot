# syntax=docker/dockerfile:1

# --- Build stage: resolve and install runtime dependencies with Poetry ---
FROM python:3.12-slim AS builder

ENV POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root --no-ansi

# --- Runtime stage: slim image with the project venv and the app code ---
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

RUN groupadd --system smilebot \
    && useradd --system --gid smilebot --home-dir /app smilebot

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --chown=smilebot:smilebot smilebot ./smilebot
COPY --chown=smilebot:smilebot migrations ./migrations

USER smilebot

CMD ["python", "-m", "smilebot"]

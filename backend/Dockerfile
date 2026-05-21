ARG PYTHON_VERSION=3.13

# --- Stage 1: Build --- #
FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./

# Use uv's own Python so the venv path is self-contained
RUN uv sync --frozen --no-dev --no-install-project

# --- Stage 2: Runtime ---
FROM python:${PYTHON_VERSION}-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=builder /app/.venv /app/.venv

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["litestar", "run", "--app", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
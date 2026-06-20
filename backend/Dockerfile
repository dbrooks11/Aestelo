ARG PYTHON_VERSION=3.13

# Stage 1: build mimalloc
FROM python:${PYTHON_VERSION}-slim-bookworm AS mimalloc-builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone -b v3.3.2 https://github.com/microsoft/mimalloc.git /mimalloc \
    && cd /mimalloc && mkdir build && cd build \
    && cmake .. && make && make install \
    && rm -rf /mimalloc

# Stage 2: install Python dependencies
FROM python:${PYTHON_VERSION}-slim-bookworm AS deps-builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

# Stage 3: runtime
FROM python:${PYTHON_VERSION}-slim-bookworm AS prod

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    LD_PRELOAD="/usr/local/lib/libmimalloc.so.3"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    libvips \
    && rm -rf /var/lib/apt/lists/*

# Copy mimalloc shared library from builder
COPY --from=mimalloc-builder /usr/local/lib/libmimalloc* /usr/local/lib/
RUN ldconfig

RUN groupadd appuser && useradd -g appuser -m appuser

COPY --from=deps-builder /app/.venv /app/.venv
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]
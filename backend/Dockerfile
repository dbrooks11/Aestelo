ARG PYTHON_VERSION=3.13

#Stage 1: Build 
FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install C/C++ build tools required to compile mimalloc
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the absolute latest mimalloc (v3.3.2) and build it from source
RUN git clone -b v3.3.2 https://github.com/microsoft/mimalloc.git /mimalloc \
    && cd /mimalloc \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

#Stage 2: Runtime
FROM python:${PYTHON_VERSION}-slim-bookworm AS prod

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=builder /app/.venv /app/.venv

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

ENV LD_PRELOAD="/usr/local/lib/libmimalloc.so.3"

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]
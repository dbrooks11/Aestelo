FROM python:3.12-slim

# Security: Prevent writing .pyc files and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Install System Dependencies (as root)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Security: Create a Non-Root User
RUN addgroup --system --gid 10001 appgroup && \
    adduser --system --uid 10001 --ingroup appgroup appuser

# 3. Create Temp Directory & Set Permissions
RUN mkdir -p /app/uploads_tmp && \
    chown -R appuser:appgroup /app/uploads_tmp

# 4. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# 5. Copy Application Code
COPY --chown=appuser:appgroup . .

# 6. Security: Switch to Non-Root User
USER appuser

# Expose the port (Flask default)
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
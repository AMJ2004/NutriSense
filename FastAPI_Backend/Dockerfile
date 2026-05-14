# backend/Dockerfile

# Build stage
FROM python:3.10-slim as builder

WORKDIR /app

COPY FastAPI_Backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt && \
    rm -rf /root/.local/lib/python*/dist-packages/tests && \
    find /root/.local -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Runtime stage
FROM python:3.10-slim

# Install only runtime essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy only necessary Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY FastAPI_Backend /app/backend
COPY Data /app/Data

WORKDIR /app/backend

# Set PATH and PYTHONPATH to use user packages
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app/backend:$PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random

# Memory optimization
ENV MALLOC_TRIM_THRESHOLD_=100000

EXPOSE 8080

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080","--workers","1","--loop","uvloop"]
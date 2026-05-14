# backend/Dockerfile

# Build stage
FROM python:3.10-slim as builder

WORKDIR /app

COPY FastAPI_Backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.10-slim

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

EXPOSE 8080

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]
# FastAPI Backend Dockerfile - Optimized for Render.com
FROM python:3.10.8-slim

RUN mkdir -p app/backend

COPY FastAPI_Backend/requirements.txt app/backend/requirements.txt
COPY Data app/Data
COPY FastAPI_Backend app/backend

WORKDIR /app/backend

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Production command (no --reload)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
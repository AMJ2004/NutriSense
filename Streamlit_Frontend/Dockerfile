# Frontend/Dockerfile

# Build stage
FROM python:3.10-slim as builder

WORKDIR /app

COPY Streamlit_Frontend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt && \
    rm -rf /root/.local/lib/python*/dist-packages/tests && \
    find /root/.local -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Runtime stage
FROM python:3.10-slim

# Copy only necessary Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY Streamlit_Frontend /app/frontend

WORKDIR /app/frontend

# Set PATH and PYTHONPATH to use user packages
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app/frontend:$PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random

# Streamlit specific settings to reduce memory usage
ENV STREAMLIT_SERVER_MAXUPLOADSIZE=200
ENV STREAMLIT_CLIENT_MAXMESSAGESIZE=200
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_ENABLEXSRFPROTECTION=false
ENV STREAMLIT_CLIENT_SHOWSTDERR=false
ENV STREAMLIT_LOGGER_LEVEL=error

# Memory optimization
ENV MALLOC_TRIM_THRESHOLD_=100000

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--logger.level=error"]

CMD ["Hello.py"]

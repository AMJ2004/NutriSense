# Frontend/Dockerfile

# Build stage
FROM python:3.10-slim as builder

WORKDIR /app

COPY Streamlit_Frontend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

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

# Streamlit specific settings to reduce memory usage
ENV STREAMLIT_SERVER_MAXUPLOADSIZE=200
ENV STREAMLIT_CLIENT_MAXMESSAGESIZE=200
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]

CMD ["Hello.py"]

# Multi-stage build for Creatio AI Knowledge Hub
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG BUILD_VERSION
ARG VCS_REF

# Labels for image metadata
LABEL maintainer="Creatio AI Knowledge Hub Team"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.version=$BUILD_VERSION
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.schema-version="1.0"

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    git \
    ffmpeg \
    tesseract-ocr \
    tesseract-ocr-eng \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements files
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    tesseract-ocr-eng \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

# Create necessary directories
RUN mkdir -p /app/ai_knowledge_hub/processed_videos \
    /app/ai_knowledge_hub/processed_pdfs \
    /app/ai_knowledge_hub/search_index \
    /app/logs \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=production

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose ports
EXPOSE 8000 8001

# Default command
CMD ["python", "-m", "uvicorn", "ai_knowledge_hub.enhanced_mcp_server:app", "--host", "0.0.0.0", "--port", "8000"]

# Development stage
FROM production as development

# Switch back to root for development dependencies
USER root

# Install development dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Install debugging tools
RUN apt-get update && apt-get install -y \
    vim \
    htop \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Switch back to appuser
USER appuser

# Override command for development
CMD ["python", "-m", "uvicorn", "ai_knowledge_hub.enhanced_mcp_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

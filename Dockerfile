# Multi-stage production Dockerfile for AutoCollective AI
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=3000

# Set working directory
WORKDIR /app

# Install curl and system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Expose web portal port
EXPOSE 3000

# Healthcheck to verify web dashboard is serving
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# Start lightweight web dashboard server
CMD ["python", "-m", "http.server", "3000", "--bind", "0.0.0.0"]

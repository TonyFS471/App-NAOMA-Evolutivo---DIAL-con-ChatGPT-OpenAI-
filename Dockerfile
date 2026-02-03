# ============================================================================
# NAOMA Evolutivo - DIAL: OpenAI Apps SDK
# Dockerfile for Railway/Fly.io/Render deployment
# ============================================================================

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Expose port
EXPOSE 8787

# Run the MCP server
CMD ["python", "-m", "app.server"]

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required by Ollama
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    sudo \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock ./

# Sync dependencies (create virtual environment)
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Add entrypoint that populates DB if missing and starts Streamlit
COPY entrypoint.sh ./
RUN chmod +x /app/entrypoint.sh

EXPOSE 8501 11434

# Run entrypoint which will start Ollama server, populate DB (if needed)
# then start Streamlit
ENTRYPOINT ["sh", "/app/entrypoint.sh"]

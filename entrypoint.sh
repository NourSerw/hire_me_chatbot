#!/bin/sh
set -e

# If running in docker-compose with separate Ollama container, OLLAMA_HOST will be set.
# If running standalone, assume Ollama is running elsewhere or will be handled separately.

# If a vector DB file or chroma DB directory already exists, skip population.
if [ -f "./vector_db/chroma.sqlite3" ] || [ -d "./chroma_db" ]; then
  echo "Vector DB already exists; skipping population"
else
  echo "Populating vector DB..."
  uv run python populate_database.py
fi

# Exec Streamlit in the uv-managed venv so signals are forwarded.
exec uv run streamlit run streamlit.py --server.port=8501 --server.address=0.0.0.0

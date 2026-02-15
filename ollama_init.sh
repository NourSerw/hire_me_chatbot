#!/bin/sh
set -e

# Start Ollama server in background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
for i in $(seq 1 60); do
  if curl -sf http://127.0.0.1:11434/v1/models >/dev/null 2>&1; then
    echo "✓ Ollama is ready"
    break
  fi
  echo "  Attempt $i/60: Waiting for Ollama..."
  sleep 1
done

# Pull mistral:7b-instruct model if not already present
echo "Checking for mistral:7b-instruct model..."
if ! ollama list 2>/dev/null | grep -q "mistral:7b-instruct"; then
  echo "Pulling mistral:7b-instruct model (may take several minutes on first run)..."
  if ollama pull mistral:7b-instruct; then
    echo "✓ Mistral:7b-instruct model pulled successfully"
  else
    echo "ERROR: Failed to pull mistral:7b-instruct model"
    exit 1
  fi
else
  echo "✓ Mistral:7b-instruct model already present"
  ollama list | grep mistral || true
fi

# Keep the Ollama process running
wait $OLLAMA_PID

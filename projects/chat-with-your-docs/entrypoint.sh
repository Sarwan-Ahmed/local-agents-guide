#!/bin/sh
set -e

if [ ! -d "/app/chroma_db" ] || [ -z "$(ls -A /app/chroma_db 2>/dev/null)" ]; then
  echo "No index found -- running ingest.py..."
  python ingest.py
fi

exec python main.py

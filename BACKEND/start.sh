#!/bin/bash
set -e

echo "================================"
echo "🎓 UNMSM SENTIMENT ANALYSIS API"
echo "================================"

# Variables de entorno
export PORT="${PORT:-8000}"
export HOST="${HOST:-0.0.0.0}"
export PYTHONUNBUFFERED=1

echo "🌐 Puerto: $PORT"
echo "🔧 Host: $HOST"
echo "📂 Directorio: $(pwd)"

# Verificar dataset
if [ ! -f "data/dataset_instagram_unmsm.csv" ]; then
    echo "❌ ERROR: Dataset no encontrado en data/"
    echo "   Por favor, asegúrate de tener el archivo:"
    echo "   data/dataset_instagram_unmsm.csv"
    exit 1
fi

echo "📊 Dataset encontrado: $(wc -l < data/dataset_instagram_unmsm.csv) líneas"

# Iniciar servidor FastAPI
echo "🚀 Iniciando servidor FastAPI..."
echo "================================"

exec uvicorn app.main:app \
    --host $HOST \
    --port $PORT \
    --workers 1 \
    --log-level info \
    --access-log \
    --no-use-colors
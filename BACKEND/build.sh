#!/bin/bash
set -e

echo "================================"
echo "🚀 BUILDING UNMSM SENTIMENT API"
echo "================================"

# 1. Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
pip install --no-cache-dir -r requirements.txt

# 2. Verificar dataset
echo "📊 Verificando dataset..."
if [ ! -f "data/dataset_instagram_unmsm.csv" ]; then
    echo "⚠️ ADVERTENCIA: Dataset no encontrado"
    echo "   Crea el directorio y asegúrate de tener el dataset"
    mkdir -p data
fi

# 3. Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p ml_models
mkdir -p reports
mkdir -p logs
mkdir -p temp

# 4. Pre-entrenar modelo si es necesario
echo "🤖 Verificando modelo ML..."
if [ ! -f "ml_models/sentiment_model.pkl" ]; then
    echo "⚠️ Modelo no encontrado, se entrenará al iniciar"
fi

echo "✅ Build completado exitosamente"
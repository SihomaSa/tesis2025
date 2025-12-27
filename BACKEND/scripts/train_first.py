# file: train_first.py
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.services.sentiment_analyzer import SentimentAnalyzer
from app.utils.config import settings

print("🚀 Entrenando y guardando el modelo...")

# 1. Inicializar el analizador
analyzer = SentimentAnalyzer()

# 2. Cargar el dataset
dataset_path = settings.DATA_DIR / settings.DATASET_FILE
print(f"📂 Buscando dataset en: {dataset_path}")

if not dataset_path.exists():
    print(f"❌ ERROR: No se encontró el dataset en {dataset_path}")
    print("   Asegúrate de que el archivo 'dataset_instagram_unmsm.csv' esté en la carpeta 'data/'.")
    exit(1)

analyzer.load_dataset(str(dataset_path))

# 3. Entrenar el modelo
print("🧠 Entrenando el modelo (esto puede tomar unos minutos)...")
analyzer.train_model()

# 4. Guardar el modelo
print("💾 Guardando modelo...")
analyzer.save_model()

print(f"✅ Modelo entrenado y guardado en: {settings.MODELS_DIR / settings.MODEL_FILE}")
print("Ahora puedes ejecutar 'test_problematic_cases.py'")
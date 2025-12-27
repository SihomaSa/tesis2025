# file: quick_fix.py
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Patch the clean_and_extract method
import app.services.sentiment_analyzer as sa

original_method = sa.AdvancedPreprocessor.clean_and_extract

def fixed_clean_and_extract(self, text):
    """Versión corregida de clean_and_extract"""
    import pandas as pd
    import re
    import numpy as np
    from typing import Dict, Tuple
    
    if pd.isna(text) or not text:
        return "", self._empty_features()
    
    text_original = str(text)
    text_lower = text_original.lower()
    
    # REGLA ESPECIAL: Textos muy cortos/cortesías simples
    def _is_very_simple_text(txt):
        txt_lower = txt.lower().strip()
        words = txt_lower.split()
        simple_courtesies = [
            'gracias', 'thanks', 'ok', 'okay', 'ya', 'entiendo', 'entendido',
            'listo', 'de acuerdo', 'vale', 'bien', 'okas', 'tqm'
        ]
        
        if len(words) <= 2:
            if all(word in simple_courtesies for word in words):
                return True
            if len(words) == 1 and len(words[0]) <= 5:
                return True
        return False
    
    if _is_very_simple_text(text_original):
        features = self._empty_features()
        features['is_very_short'] = 1
        features['word_count'] = len(text_lower.split())
        features['is_simple_courtesy'] = 1
        features['overall_sentiment'] = 0.0
        return text_lower, features
    
    # Si no es texto simple, llamar al método original
    return original_method(self, text)

# Monkey patch the method
sa.AdvancedPreprocessor.clean_and_extract = fixed_clean_and_extract

print("✅ Método clean_and_extract parcheado")

# Now run the training
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.utils.config import settings

print("🚀 Entrenando y guardando el modelo...")
analyzer = SentimentAnalyzer()

dataset_path = settings.DATA_DIR / settings.DATASET_FILE
print(f"📂 Buscando dataset en: {dataset_path}")

if not dataset_path.exists():
    print(f"❌ ERROR: No se encontró el dataset en {dataset_path}")
    print("   Asegúrate de que el archivo 'dataset_instagram_unmsm.csv' esté en la carpeta 'data/'.")
    exit(1)

analyzer.load_dataset(str(dataset_path))
print("🧠 Entrenando el modelo (esto puede tomar unos minutos)...")
analyzer.train_model()
print("💾 Guardando modelo...")
analyzer.save_model()
print(f"✅ Modelo entrenado y guardado en: {settings.MODELS_DIR / settings.MODEL_FILE}")
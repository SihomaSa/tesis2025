FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Eliminar config.py problemático y crear uno nuevo
RUN rm -f app/utils/config.py

# Crear config.py simple y completo
RUN cat > app/utils/config.py << 'EOF'
from typing import List
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    # Servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    ALLOWED_ORIGINS: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    
    # Rutas
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "ml_models"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    TEMP_DIR: Path = BASE_DIR / "temp"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # ML
    MODEL_TYPE: str = "ensemble"
    TEST_SIZE: float = 0.2
    RANDOM_STATE: int = 42
    N_JOBS: int = -1
    
    # TF-IDF
    TFIDF_MAX_FEATURES: int = 200
    TFIDF_MIN_DF: int = 2
    TFIDF_MAX_DF: float = 0.9
    TFIDF_NGRAM_RANGE: tuple = (1, 3)
    
    # Umbrales
    NEGATIVE_THRESHOLD: float = 0.35
    POSITIVE_THRESHOLD: float = 0.45
    
    # Para evitar warning de pydantic
    model_config = {"protected_namespaces": ()}

settings = Settings()

# Diccionarios completos (simplificados pero funcionales)
EMOTICONES_SENTIMENT = {
    '😂': 5, '🤣': 5, '😍': 5, '🥰': 5, '❤️': 5, '💖': 5,
    '😢': -5, '😭': -5, '😠': -5, '😡': -5, '🤬': -5, '💔': -5,
    '👏': 4, '✨': 4, '🌟': 4, '👍': 4, '👎': -5,
    '😀': 3, '😃': 3, '😄': 3, '😊': 4, '😘': 4,
    '😒': -4, '😓': -4, '😞': -4, '😟': -4
}

JERGAS_PERUANAS = {
    'bacán': 5, 'bacan': 5, 'buenazo': 5, 'chévere': 5, 'chevere': 5,
    'genial': 5, 'crack': 5, 'trome': 5, 'mostro': 5,
    'roche': -5, 'palta': -5, 'palteado': -5, 'piña': -5, 'malazo': -5
}

PALABRAS_POSITIVAS = {
    'excelente': 5, 'increíble': 5, 'maravilloso': 5, 'fantástico': 5,
    'genial': 5, 'perfecto': 5, 'extraordinario': 5, 'excepcional': 5,
    'bueno': 4, 'buena': 4, 'feliz': 4, 'alegre': 4, 'contento': 4,
    'gracias': 4, 'amor': 4, 'orgullo': 4, 'éxito': 4, 'logro': 4
}

PALABRAS_NEGATIVAS = {
    'pésimo': -5, 'horrible': -5, 'terrible': -5, 'espantoso': -5,
    'desastre': -5, 'fatal': -5, 'odio': -5, 'asco': -5,
    'malo': -4, 'mala': -4, 'problema': -4, 'fallo': -4, 'error': -4,
    'triste': -4, 'decepción': -4, 'decepcionante': -4
}

PATRONES_NEGATIVOS = {
    'no sirve': -5, 'no funciona': -5, 'no me gusta': -4,
    'pésimo servicio': -5, 'horrible atención': -5, 'mala calidad': -4
}

INTENSIFICADORES = {
    'muy': 1.8, 'mucho': 1.8, 'demasiado': 1.8,
    'super': 1.8, 'súper': 1.8, 'ultra': 1.8,
    'tan': 1.5, 'tanto': 1.5, 'extremadamente': 1.8
}

PATRONES_POSITIVOS = {
    'felicidades a': 5, 'felicitaciones a': 5, 'orgullo de': 5,
    'excelente trabajo': 5, 'buen trabajo': 4, 'lo máximo': 5
}

PATRONES_NEUTROS = {
    'cuándo es': 0, 'dónde está': 0, 'cómo hacer': 0,
    'qué hora': 0, 'información sobre': 0
}

CONTEXTOS_COMPLEJOS = {
    'a pesar de': {'neg_score': -2, 'pos_score': 3}
}

NEGACIONES = ['no', 'nunca', 'jamás', 'tampoco', 'ni', 'sin']

STOP_WORDS_SPANISH = [
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se',
    'las', 'un', 'por', 'con', 'para', 'una', 'su', 'al', 'lo',
    'es', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este'
]
EOF

# Copiar el resto de la aplicación
COPY . .

# Crear directorios
RUN mkdir -p logs data ml_models reports temp

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
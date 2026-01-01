"""
CONFIGURACIÓN DEL SISTEMA - UNMSM SENTIMENT ANALYSIS
Versión simplificada sin pydantic-settings
"""

from typing import List
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    """Configuración global del sistema"""
    
    # Información del Proyecto
    PROJECT_NAME: str = "UNMSM Sentiment Analysis"
    PROJECT_VERSION: str = "3.1.0"
    PROJECT_DESCRIPTION: str = "Sistema de Análisis de Sentimientos para Instagram UNMSM"
    
    # Servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://localhost:4201",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:4201",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    # Timeouts (en segundos)
    API_TIMEOUT: int = 30
    DEFAULT_TIMEOUT: int = 10
    
    # Rutas de datos
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "ml_models"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    TEMP_DIR: Path = BASE_DIR / "temp"
    
    # Nombres de archivos
    DATASET_FILE: str = "dataset_instagram_unmsm.csv"
    MODEL_FILE: str = "sentiment_model.pkl"
    PREPROCESSOR_FILE: str = "preprocessor.pkl"
    VECTORIZER_FILE: str = "tfidf_vectorizer.pkl"
    SCALER_FILE: str = "scaler.pkl"
    
    # Configuración del Modelo ML
    MODEL_TYPE: str = "ensemble"
    TEST_SIZE: float = 0.2
    RANDOM_STATE: int = 42
    N_JOBS: int = -1
    
    # Configuración de TF-IDF
    TFIDF_MAX_FEATURES: int = 200
    TFIDF_MIN_DF: int = 2
    TFIDF_MAX_DF: float = 0.9
    TFIDF_NGRAM_RANGE: tuple = (1, 3)
    
    # Umbrales de confianza
    CONFIDENCE_THRESHOLD_HIGH: float = 0.75
    CONFIDENCE_THRESHOLD_MEDIUM: float = 0.50
    
    # Umbrales de clasificación
    NEGATIVE_THRESHOLD: float = 0.35
    POSITIVE_THRESHOLD: float = 0.45
    
    # Límites de procesamiento
    MAX_BATCH_SIZE: int = 1000
    MAX_COMMENT_LENGTH: int = 500
    
    # Caché
    ENABLE_CACHE: bool = True
    CACHE_TTL: int = 3600
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/sentiment_analysis.log"
    
    # Base de datos (opcional)
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "unmsm_sentiment"
    
    # Seguridad
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60
    
    # Configuración de reportes
    REPORT_EXPORT_FORMATS: List[str] = ["pdf", "xlsx", "json"]
    REPORT_MAX_RECORDS: int = 10000
    
    # Para evitar warning de pydantic
    model_config = {"protected_namespaces": ()}

# Crear instancia
settings = Settings()

# Crear directorios si no existen
def create_directories():
    """Crea los directorios necesarios"""
    directories = [
        settings.DATA_DIR,
        settings.MODELS_DIR,
        settings.REPORTS_DIR,
        settings.TEMP_DIR,
        BASE_DIR / "logs"
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

create_directories()

# ============================================================================
# DICCIONARIOS DE SENTIMIENTO
# ============================================================================

EMOTICONES_SENTIMENT = {
    '😂': 5, '🤣': 5, '😍': 5, '🥰': 5, '❤️': 5, '💖': 5, '🔥': 5, '💯': 5,
    '👏': 4, '✨': 4, '🌟': 4, '👍': 4, '😊': 4, '😘': 4,
    '😀': 3, '😃': 3, '😄': 3,
    '😢': -5, '😭': -5, '😠': -5, '😡': -5, '🤬': -5, '💔': -5, '👎': -5,
    '😒': -4, '😓': -4, '😞': -4, '😟': -4,
    '😅': 0, '🙃': 0, '😏': 0, '🤔': 0
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
    'gracias': 4, 'amor': 4, 'orgullo': 4, 'éxito': 4, 'logro': 4,
    'hermoso': 4, 'lindo': 4, 'bonito': 4
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
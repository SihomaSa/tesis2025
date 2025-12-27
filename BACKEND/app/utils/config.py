"""
CONFIGURACIÓN DEL SISTEMA - UNMSM SENTIMENT ANALYSIS
VERSIÓN CORREGIDA - Pesos balanceados
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
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
        "http://127.0.0.1:4201"
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
    
    # Umbrales de clasificación - AJUSTADOS
    NEGATIVE_THRESHOLD: float = 0.35  # Más estricto
    POSITIVE_THRESHOLD: float = 0.45  # Más permisivo
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Crear instancia de configuración
settings = Settings()

# Crear directorios si no existen
def create_directories():
    """Crea los directorios necesarios para el sistema"""
    directories = [
        settings.DATA_DIR,
        settings.MODELS_DIR,
        settings.REPORTS_DIR,
        settings.TEMP_DIR,
        BASE_DIR / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Ejecutar creación de directorios al importar
create_directories()

# ============================================================================
# DICCIONARIOS DE SENTIMIENTO - PESOS BALANCEADOS
# ============================================================================

EMOTICONES_SENTIMENT = {
    # Positivos muy fuertes
    '😂': 5, '🤣': 5, '😍': 5, '🥰': 5, '❤️': 5, '💖': 5, '🔥': 5, '💯': 5,
    '🙌': 5, '🏆': 5, '🎉': 5, '🥳': 5, '🤩': 5, '😻': 5, '💝': 5, '🫶': 5,
    # Positivos fuertes
    '👏': 4, '✨': 4, '🌟': 4, '💪': 4, '👍': 4, '👌': 4, '🙏': 4, '🎓': 4,
    '💕': 4, '💗': 4, '⭐': 4, '🌈': 4, '☀️': 4, '💫': 4, '😊': 4, '😘': 4,
    # Positivos leves
    '😀': 3, '😃': 3, '😄': 3, '😁': 3, '😆': 3, '🙂': 3, '🤗': 3, '😇': 3,
    # Negativos muy fuertes
    '😢': -5, '😭': -5, '😠': -5, '😡': -5, '🤬': -5, '💔': -5, '🤢': -5,
    '🤮': -5, '😱': -5, '👎': -5, '💀': -5, '☠️': -5,
    # Negativos fuertes
    '😒': -4, '😓': -4, '😞': -4, '😟': -4, '😤': -4, '📉': -4, '😩': -4,
    '😫': -4, '🥺': -3, '⚠️': -4, '🚫': -4, '❌': -4,
    # Negativos leves
    '😐': -2, '😑': -2, '😕': -2, '🙁': -2, '☹️': -2, '😪': -2,
    # Neutrales
    '😅': 0, '🙃': 0, '😏': 0, '🤔': 0, '🤨': 0, '😬': 0
}

JERGAS_PERUANAS = {
    # Positivas muy fuertes (aumentadas de 4 a 5)
    'bacán': 5, 'bacan': 5, 'buenazo': 5, 'chévere': 5, 'chevere': 5,
    'genial': 5, 'crack': 5, 'trome': 5, 'mostro': 5, 'ídolo': 5,
    # Positivas fuertes
    'pata': 4, 'causa': 4, 'broder': 4, 'jato': 4, 'fresh': 4,
    'arriba': 4, 'vamos': 4, 'dale': 4,
    # Expresiones de risa
    'jajaja': 4, 'jajajaja': 4, 'jaja': 4, 'jeje': 4, 'xd': 4, 'XD': 4,
    # Negativas muy fuertes
    'roche': -5, 'palta': -5, 'palteado': -5, 'piña': -5, 'malazo': -5,
    'fregado': -5, 'webada': -5, 'odio': -5, 'asco': -5,
    # Negativas fuertes
    'asado': -4, 'misio': -4, 'me llega': -5, 'llega': -4,
    # UNMSM específicas
    'jerí': -3, 'jeri': -3, 'scopus': -2, 'sunedu': -2
}

# PALABRAS POSITIVAS - PESOS AUMENTADOS
PALABRAS_POSITIVAS = {
    # Muy positivas (aumentadas de 4 a 5)
    'excelente': 5, 'increíble': 5, 'maravilloso': 5, 'fantástico': 5,
    'genial': 5, 'perfecto': 5, 'extraordinario': 5, 'excepcional': 5,
    'sobresaliente': 5, 'magnífico': 5, 'espectacular': 5,
    
    # Positivas fuertes (aumentadas de 3 a 4)
    'bueno': 4, 'buena': 4, 'buenos': 4, 'buenas': 4,
    'feliz': 4, 'alegre': 4, 'contento': 4, 'contenta': 4,
    'gracias': 4, 'amor': 4, 'orgullo': 4, 'orgulloso': 4,
    'éxito': 4, 'logro': 4, 'mejor': 4, 'mejora': 4,
    'hermoso': 4, 'hermosa': 4, 'bello': 4, 'bella': 4,
    'bonito': 4, 'bonita': 4, 'lindo': 4, 'linda': 4,
    'primera': 4, 'primero': 4, 'líder': 4, 'top': 4,
    'prestigio': 4, 'prestigiosa': 4, 'calidad': 4, 
    'eficiente': 4, 'eficaz': 4,
    
    # Positivas moderadas
    'agradable': 3, 'satisfecho': 3, 'satisfecha': 3,
    'recomendable': 3, 'recomiendo': 3, 'positivo': 3,
    'agradecido': 3, 'agradecida': 3, 'favorable': 3,
    
    # Educación específica
    'profesores': 3, 'profesor': 3, 'docente': 3, 'docentes': 3,
    'enseñanza': 3, 'aprendizaje': 3, 'formación': 3,
    'conocimiento': 3, 'académico': 3, 'académica': 3,
    
    # Nuevas palabras de los comentarios - MUY POSITIVAS
    'felicitaciones': 5, 'bravo': 5, 'grande': 5, 'campeones': 5,
    'crack': 5, 'cracks': 5, 'capo': 5, 'ídolo': 5,
    'bendiciones': 5, 'admiración': 5, 'fascinante': 5,
    
    # POSITIVAS FUERTES
    'orgullo': 4, 'orgullosa': 4, 'orgulloso': 4, 'orgullosamente': 4,
    'merecido': 4, 'brillante': 4, 'exitoso': 4, 'exitosa': 4,
    'promesa': 4, 'triunfo': 4, 'campeón': 4, 'campeon': 4,
    'innovador': 4, 'innovadora': 4, 'talento': 4, 'talentoso': 4,
    'esfuerzo': 4, 'dedicación': 4, 'compromiso': 4,
    'histórico': 4, 'histórica': 4, 'importante': 4,
    'relevante': 4, 'destacado': 4, 'destacada': 4,
    'reconocimiento': 4, 'reconocido': 4, 'reconocida': 4,
    'aporte': 4, 'contribución': 4, 'valioso': 4, 'valiosa': 4,
    'bendición': 4, 'suerte': 4, 'fortuna': 4,
    'inspirador': 4, 'inspiradora': 4, 'motivador': 4,
    'impresionante': 4, 'notable': 4, 'admirable': 4,
    'beca': 4, 'becado': 4, 'premio': 4, 'premiado': 4,
    'oportunidad': 4, 'potencial': 4, 'promesa': 4,
    
    # POSITIVAS MODERADAS (sentimientos/emociones)
    'emoción': 3, 'emociona': 3, 'emocionante': 3,
    'alegría': 3, 'felicidad': 3, 'satisfacción': 3,
    'entusiasmo': 3, 'entusiasta': 3, 'animado': 3,
    'ilusión': 3, 'esperanza': 3, 'optimismo': 3,
    'confianza': 3, 'seguridad': 3, 'tranquilidad': 3,
    'agradecimiento': 3, 'aprecio': 3, 'gratitud': 3,
    'cariño': 3, 'afecto': 3, 'respeto': 3,
    'admiración': 3, 'valoración': 3, 'consideración': 3,
    
    # EDUCACIÓN Y ACADEMIA (más específicas)
    'investigación': 3, 'investigador': 3, 'científico': 3,
    'estudio': 3, 'estudiante': 3, 'alumno': 3,
    'universidad': 3, 'universitario': 3, 'académico': 3,
    'doctorado': 3, 'maestría': 3, 'posgrado': 3,
    'tesis': 3, 'proyecto': 3, 'desarrollo': 3,
    'capacitación': 3, 'entrenamiento': 3, 'preparación': 3,
    'competencia': 3, 'habilidad': 3, 'destreza': 3,
    
    # VERBOS POSITIVOS
    'avanza': 3, 'avanzar': 3, 'progresa': 3, 'progresar': 3,
    'mejora': 3, 'mejorar': 3, 'crece': 3, 'crecer': 3,
    'fortalece': 3, 'fortalecer': 3, 'impulsa': 3, 'impulsar': 3,
    'apoya': 3, 'apoyar': 3, 'ayuda': 3, 'ayudar': 3,
    'contribuye': 3, 'contribuir': 3, 'facilita': 3, 'facilitar': 3,
    'beneficia': 3, 'beneficiar': 3, 'favorece': 3, 'favorecer': 3,
    'enorgullece': 4, 'enorgullecer': 4, 'destaca': 4, 'destacar': 4,
    'sobresale': 4, 'sobresalir': 4, 'triunfa': 4, 'triunfar': 4,
    
    # EXPRESIONES COLOQUIALES POSITIVAS
    'épico': 4, 'golazo': 4, 'god': 4, 'joya': 4,
    'fino': 3, 'fino señores': 4, 'de lujo': 4,
    'tremendo': 4, 'terrible': 3, 'bestial': 4,
    'asu': 3, 'wow': 4, 'omg': 4, 'uff': 3,
    'pro': 4, 'master': 4, 'legend': 4, 'titan': 4,
    'champion': 4, 'boss': 4, 'rey': 4, 'reina': 4
}

# PALABRAS NEGATIVAS - MANTENIDAS IGUAL
PALABRAS_NEGATIVAS = {
    'pésimo': -5, 'horrible': -5, 'terrible': -5, 'espantoso': -5,
    'desastre': -5, 'fatal': -5, 'odio': -5, 
    'malo': -4, 'mala': -4, 'malos': -4, 'malas': -4,
    'problema': -4, 'problemas': -4, 'fallo': -4, 'error': -4,
    'triste': -4, 'decepción': -4, 'decepcionante': -4,
    'molesto': -4, 'molesta': -4, 'enojo': -4,
    'peor': -3, 'crítica': -3, 'queja': -3, 'reclamo': -3,
    'deficiente': -3, 'inadecuado': -3, 'lento': -3, 'difícil': -3, 
    'normal': -1, 'promedio': -1,
    
    # NUEVAS PALABRAS NEGATIVAS de los comentarios
    # Muy negativas
    'vergonzoso': -5, 'vergüenza': -5, 'indignante': -5, 'indigna': -5,
    'aberración': -5, 'atrocidad': -5, 'desgracia': -5, 'catástrofe': -5,
    'lamentable': -4, 'deplorable': -4, 'inaceptable': -4, 'intolerable': -4,
    'desastroso': -5, 'caótico': -4, 'pésimo': -5, 'deficiente': -4,
    
    # Negativas fuertes (gestión/administración)
    'fracaso': -4, 'fracasado': -4, 'incompetente': -5, 'incompetencia': -5,
    'ineficiente': -4, 'ineficaz': -4, 'negligente': -5, 'negligencia': -5,
    'corrupto': -5, 'corrupción': -5, 'robo': -5, 'fraude': -5,
    'malversación': -5, 'impunidad': -5, 'abuso': -5,
    'gestión': -2, 'mala gestión': -5, 'pésima gestión': -5,
    
    # Conflicto/violencia
    'violencia': -5, 'violento': -5, 'agresión': -5, 'agredir': -5,
    'golpe': -4, 'golpear': -4, 'ataque': -4, 'atacar': -4,
    'represión': -5, 'reprimir': -5, 'matones': -5, 'sicarios': -5,
    'amenaza': -4, 'amenazar': -4, 'intimidación': -4, 'intimidar': -4,
    'conflicto': -3, 'enfrentamiento': -3, 'pelea': -3,
    
    # Protesta/descontento
    'protesta': -2, 'reclamo': -3, 'queja': -3, 'denuncia': -3,
    'indignación': -4, 'indignado': -4, 'molesto': -3, 'enojado': -4,
    'frustración': -3, 'frustrado': -3, 'descontento': -3,
    'injusticia': -4, 'injusto': -4, 'discriminación': -5,
    
    # Inseguridad
    'robo': -5, 'robaron': -5, 'robado': -5, 'roban': -5,
    'inseguridad': -4, 'inseguro': -4, 'peligro': -4, 'peligroso': -4,
    'riesgo': -3, 'amenaza': -4, 'vulnerabilidad': -3,
    
    # Calidad/servicio
    'deficiente': -4,
}

PATRONES_NEGATIVOS = {
    'no sirve': -5, 'no funciona': -5, 'no trabaj': -4,
    'no me gusta': -4, 'no recomiendo': -4, 'qué mal': -4,
    'pésimo servicio': -5, 'horrible atención': -5, 'mala calidad': -4,
    'muy mal': -4, 'muy malo': -4, 'muy mala': -4
}

INTENSIFICADORES = {
    'muy': 1.8, 'mucho': 1.8, 'mucha': 1.8, 'muchos': 1.8,
    'demasiado': 1.8, 'bastante': 1.5,
    'super': 1.8, 'súper': 1.8, 'ultra': 1.8, 'mega': 1.8,
    'tan': 1.5, 'tanto': 1.5, 'tanta': 1.5,
    'sumamente': 1.8, 'extremadamente': 1.8,
    'increíblemente': 1.8, 'realmente': 1.5
}

PATRONES_POSITIVOS = {
    'felicidades a': 5, 'felicitaciones a': 5, 'felicitaciones por': 5,
    'orgullo de': 5, 'orgulloso de': 5, 'orgullosa de': 5,
    'excelente trabajo': 5, 'buen trabajo': 4, 'gran trabajo': 5,
    'que bien': 4, 'lo máximo': 5, 'eres un capo': 5,
    'me encanta': 4, 'me gusta': 3, 'me fascina': 4,
    'vamos unmsm': 5, 'vamos san marcos': 5, 'vamos decana': 5,
    'sigue así': 4, 'continúa así': 4, 'adelante': 3,
    'éxito total': 5, 'completamente exitoso': 4,
    'lo mejor': 5, 'de lo mejor': 4, 'de primera': 4,
    'increíblemente bueno': 5, 'realmente bueno': 4,
    'sobresaliente trabajo': 5, 'destacado': 4,
    'siempre san marcos': 5, 'siempre san marquina': 5,
    'decana de américa': 5, 'alma mater': 4,
    'nro 1': 5, 'número uno': 5, 'num 1': 5,
}

PATRONES_NEUTROS = {
    'cuándo es': 0, 'dónde está': 0, 'cómo hacer': 0,
    'qué hora': 0, 'a qué hora': 0, 'horario de': 0,
    'información sobre': 0, 'info de': 0, 'datos de': 0,
    'link de': 0, 'enlace de': 0, 'url de': 0,
    'consulta sobre': 0, 'pregunta sobre': 0,
    'saber más': 0, 'más información': 0,
    'explicación de': 0, 'detalles de': 0,
    'y en el': 0, 'qué pasa con': 0,
    'igual está bien': 0, 'está bien': 0,
    'hasta donde sé': 0, 'según entiendo': 0,
    'ok gracias': 0, 'gracias ok': 0,
    'entendido gracias': 0, 'de acuerdo': 0,
    'gracias': 0, 'thanks': 0, 'tqm': 0,
    'ok': 0, 'okay': 0, 'ya': 0, 'entiendo': 0, 'entendido': 0,
    'de acuerdo': 0, 'está bien': 0, 'esta bien': 0,
    'hasta donde sé': 0, 'según entiendo': 0,
    'depende del': 0, 'según el': 0, 'en función de': 0,
    'a pesar de': -1,  # Esto indica conflicto
    'siempre san': 2,  # Esto es positivo
}

CONTEXTOS_COMPLEJOS = {
    'a pesar de': {'neg_score': -2, 'pos_score': 3},  # Negativo al inicio, positivo después
    'pero igual': {'neg_score': -1, 'pos_score': 1},  # Balanceado
    'sin embargo': {'neg_score': -1, 'pos_score': 1},  # Contraste
}

NEGACIONES = [
    'no', 'nunca', 'jamás', 'tampoco', 'ni', 'sin', 
    'ningún', 'ninguna', 'nada', 'nadie'
]

# Stop words en español
STOP_WORDS_SPANISH = [
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se',
    'las', 'un', 'por', 'con', 'para', 'una', 'su', 'al', 'lo',
    'es', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este',
    'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre',
    'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde',
    'ha', 'han', 'son', 'está', 'están'
]


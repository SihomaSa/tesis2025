"""
DEPENDENCIAS DEL SISTEMA - API UNMSM
Gestión centralizada de dependencias para evitar imports circulares
"""

from fastapi import HTTPException
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

# Variable global del analizador (se establecerá desde main.py)
_sentiment_analyzer: Optional[Any] = None

def set_analyzer(analyzer: Any) -> None:
    """
    Establece el analizador desde main.py
    
    Args:
        analyzer: Instancia de SentimentAnalyzer
    """
    global _sentiment_analyzer
    _sentiment_analyzer = analyzer
    logger.info("✅ Analizador configurado en dependencias")

def get_sentiment_analyzer() -> Any:
    """
    Obtiene la instancia del analizador de sentimientos
    
    Returns:
        Instancia de SentimentAnalyzer
        
    Raises:
        HTTPException: Si el analizador no está inicializado
    """
    global _sentiment_analyzer
    
    if _sentiment_analyzer is None:
        logger.error("❌ Intento de acceder al analizador antes de inicialización")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Service Unavailable",
                "message": "El analizador de sentimientos no está inicializado",
                "suggestion": "Por favor espera a que el sistema termine de iniciar"
            }
        )
    
    return _sentiment_analyzer

def is_analyzer_ready() -> bool:
    """
    Verifica si el analizador está listo
    
    Returns:
        True si el analizador está inicializado, False en caso contrario
    """
    global _sentiment_analyzer
    return _sentiment_analyzer is not None
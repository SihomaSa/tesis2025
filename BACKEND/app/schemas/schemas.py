"""
SCHEMAS - Modelos Pydantic para API UNMSM
✅ Configuración correcta para serialización JSON
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime


# ============================================================================
# MODELOS BASE
# ============================================================================

class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "error": "Error al procesar la solicitud",
                "detail": "Descripción detallada del error",
                "timestamp": "2025-01-01T12:00:00"
            }
        }
    )


# ============================================================================
# MODELOS DE ANÁLISIS INDIVIDUAL
# ============================================================================

class AnalysisRequest(BaseModel):
    """Request para análisis individual"""
    comment: str = Field(..., min_length=1, max_length=5000, description="Comentario a analizar")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "comment": "Excelente universidad, la mejor del país"
            }
        }
    )


class SentimentProbabilities(BaseModel):
    """Probabilidades de cada sentimiento"""
    negativo: float = Field(..., ge=0, le=1)
    neutral: float = Field(..., ge=0, le=1)
    positivo: float = Field(..., ge=0, le=1)


class AnalysisResponse(BaseModel):
    """Respuesta de análisis individual"""
    success: bool = True
    comment: str
    sentimiento: str
    confianza: float = Field(..., ge=0, le=1)
    probabilities: SentimentProbabilities
    timestamp: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "comment": "Excelente universidad",
                "sentimiento": "Positivo",
                "confianza": 0.95,
                "probabilities": {
                    "negativo": 0.02,
                    "neutral": 0.03,
                    "positivo": 0.95
                },
                "timestamp": "2025-01-01T12:00:00"
            }
        }
    )


# ============================================================================
# MODELOS DE REPORTES
# ============================================================================

class ReportRequest(BaseModel):
    """Request para generar reporte"""
    period: Literal["current", "last", "quarter", "year", "custom"] = "current"
    format: Literal["json", "pdf", "excel"] = "json"
    include_details: bool = True
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "period": "current",
                "format": "json",
                "include_details": True
            }
        }
    )


class ReportSummary(BaseModel):
    """Resumen ejecutivo del reporte"""
    total_comments: int = Field(..., ge=0)
    positive_count: int = Field(..., ge=0)
    neutral_count: int = Field(..., ge=0)
    negative_count: int = Field(..., ge=0)
    positive_percentage: float = Field(..., ge=0, le=100)
    negative_percentage: float = Field(..., ge=0, le=100)
    neutral_percentage: float = Field(..., ge=0, le=100)
    general_perception: Literal["positiva", "neutral", "negativa"]
    engagement_rate: float = Field(..., ge=0)
    model_confidence: float = Field(..., ge=0, le=100)
    avg_comment_length: float = Field(..., ge=0)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_comments": 1500,
                "positive_count": 1000,
                "neutral_count": 300,
                "negative_count": 200,
                "positive_percentage": 66.7,
                "negative_percentage": 13.3,
                "neutral_percentage": 20.0,
                "general_perception": "positiva",
                "engagement_rate": 8.5,
                "model_confidence": 85.0,
                "avg_comment_length": 120.5
            }
        }
    )


class ReportStatistics(BaseModel):
    """Estadísticas detalladas"""
    sentiment_distribution: Dict[str, int]
    avg_comment_length: float = Field(..., ge=0)
    total_words: int = Field(..., ge=0)
    unique_words: int = Field(..., ge=0)
    most_common_words: List[tuple] = Field(default_factory=list)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sentiment_distribution": {
                    "Positivo": 1000,
                    "Neutral": 300,
                    "Negativo": 200
                },
                "avg_comment_length": 120.5,
                "total_words": 15000,
                "unique_words": 2500,
                "most_common_words": [
                    ["universidad", 450],
                    ["excelente", 380],
                    ["calidad", 320]
                ]
            }
        }
    )


class CategoryScore(BaseModel):
    """Score por categoría"""
    name: str
    score: int = Field(..., ge=0, le=100)
    description: str
    positive_count: int = Field(..., ge=0)
    neutral_count: int = Field(..., ge=0)
    negative_count: int = Field(..., ge=0)
    total_count: int = Field(..., ge=0)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Enseñanza",
                "score": 85,
                "description": "Calidad docente y metodologías de enseñanza",
                "positive_count": 850,
                "neutral_count": 100,
                "negative_count": 50,
                "total_count": 1000
            }
        }
    )


class ReportInsight(BaseModel):
    """Insight del reporte"""
    type: Literal["positive", "warning", "info", "critical"]
    title: str
    description: str
    metric: float
    icon: str = "ℹ"
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "positive",
                "title": "Percepción Positiva Dominante",
                "description": "Los comentarios positivos representan el 66.7% del total",
                "metric": 66.7,
                "icon": "✓"
            }
        }
    )


class ReportRecommendation(BaseModel):
    """Recomendación del reporte"""
    category: Literal["potenciar", "mejorar", "monitorear", "urgente"]
    title: str
    items: List[str]
    priority: Literal["high", "medium", "low"]
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "category": "potenciar",
                "title": "Áreas a Potenciar",
                "items": [
                    "Contenido sobre excelencia docente",
                    "Historias de éxito de estudiantes"
                ],
                "priority": "high"
            }
        }
    )


class WordTag(BaseModel):
    """Palabra para nube de palabras"""
    text: str
    size: int = Field(..., ge=10, le=40)
    count: int = Field(..., ge=1)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Universidad",
                "size": 24,
                "count": 450
            }
        }
    )


class ReportResponse(BaseModel):
    """Respuesta completa del reporte"""
    success: bool = True
    title: str
    period: str
    period_text: str
    generated_at: str
    summary: ReportSummary
    statistics: ReportStatistics
    categories: List[CategoryScore]
    insights: List[ReportInsight]
    recommendations: List[ReportRecommendation]
    top_words: List[WordTag]
    best_day: str
    best_day_engagement: float
    best_time: str
    best_time_range: str
    error: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "success": True,
                "title": "Reporte de Análisis de Sentimientos - UNMSM",
                "period": "current",
                "period_text": "Diciembre 2025",
                "generated_at": "2025-01-01T12:00:00",
                "summary": {
                    "total_comments": 1500,
                    "positive_count": 1000,
                    "neutral_count": 300,
                    "negative_count": 200,
                    "positive_percentage": 66.7,
                    "negative_percentage": 13.3,
                    "neutral_percentage": 20.0,
                    "general_perception": "positiva",
                    "engagement_rate": 8.5,
                    "model_confidence": 85.0,
                    "avg_comment_length": 120.5
                },
                "best_day": "Miércoles",
                "best_day_engagement": 127.5,
                "best_time": "10:00 AM - 12:00 PM",
                "best_time_range": "10:00 AM y 12:00 PM"
            }
        }
    )


# ============================================================================
# MODELOS DE ESTADÍSTICAS
# ============================================================================

class DatasetInfo(BaseModel):
    """Información del dataset"""
    total_comments: int = Field(..., ge=0)
    distribution: Dict[str, int]
    percentages: Dict[str, float]
    avg_comment_length: float = Field(..., ge=0)
    most_common_words: List[tuple]
    columns: List[str]
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_comments": 1500,
                "distribution": {
                    "Positivo": 1000,
                    "Neutral": 300,
                    "Negativo": 200
                },
                "percentages": {
                    "Positivo": 66.7,
                    "Neutral": 20.0,
                    "Negativo": 13.3
                },
                "avg_comment_length": 120.5,
                "most_common_words": [
                    ["universidad", 450],
                    ["excelente", 380]
                ],
                "columns": ["texto_comentario", "sentimiento"]
            }
        }
    )


class ModelInfo(BaseModel):
    """Información del modelo"""
    is_trained: bool
    model_metadata: Dict[str, Any]
    has_model: bool
    has_vectorizer: bool
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "is_trained": True,
                "model_metadata": {
                    "accuracy": 0.85,
                    "model_type": "RandomForest",
                    "training_date": "2025-01-01T12:00:00"
                },
                "has_model": True,
                "has_vectorizer": True
            }
        }
    )


# ============================================================================
# MODELOS DE UTILIDAD
# ============================================================================

class PeriodOption(BaseModel):
    """Opción de período"""
    value: str
    label: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "value": "current",
                "label": "Mes Actual"
            }
        }
    )


class HealthCheck(BaseModel):
    """Health check del servicio"""
    status: str = "healthy"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    version: str = "3.0.0"
    services: Dict[str, bool] = Field(default_factory=dict)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "timestamp": "2025-01-01T12:00:00",
                "version": "3.0.0",
                "services": {
                    "analyzer": True,
                    "database": True
                }
            }
        }
    )
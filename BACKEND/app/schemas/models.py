"""
SCHEMAS Y MODELOS DE DATOS - API UNMSM
Definición de estructuras de datos para requests y responses
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class SentimentType(str, Enum):
    """Tipos de sentimiento"""
    POSITIVO = "Positivo"
    NEUTRAL = "Neutral"
    NEGATIVO = "Negativo"


class ConfidenceLevel(str, Enum):
    """Niveles de confianza"""
    HIGH = "Alta"
    MEDIUM = "Media"
    LOW = "Baja"


# ========== REQUEST SCHEMAS ==========

class CommentAnalysisRequest(BaseModel):
    """Request para análisis de comentario individual"""
    comment: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Comentario a analizar",
        example="La universidad tiene excelentes profesores"
    )
    
    @validator('comment')
    def validate_comment(cls, v):
        if not v.strip():
            raise ValueError("El comentario no puede estar vacío")
        return v.strip()


class BatchAnalysisRequest(BaseModel):
    """Request para análisis por lote"""
    comments: List[str] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="Lista de comentarios a analizar",
        example=[
            "Excelente universidad",
            "Pésimo servicio",
            "Ambiente regular"
        ]
    )
    
    @validator('comments')
    def validate_comments(cls, v):
        if not v:
            raise ValueError("La lista de comentarios no puede estar vacía")
        # Filtrar comentarios vacíos
        filtered = [c.strip() for c in v if c and c.strip()]
        if not filtered:
            raise ValueError("No hay comentarios válidos en la lista")
        return filtered


class DatasetUploadRequest(BaseModel):
    """Request para cargar dataset"""
    file_path: str = Field(
        ...,
        description="Ruta del archivo CSV",
        example="data/dataset_instagram_unmsm.csv"
    )


# ========== RESPONSE SCHEMAS ==========

class SentimentProbabilities(BaseModel):
    """Probabilidades de cada sentimiento"""
    negativo: float = Field(..., ge=0, le=1, description="Probabilidad negativo")
    neutral: float = Field(..., ge=0, le=1, description="Probabilidad neutral")
    positivo: float = Field(..., ge=0, le=1, description="Probabilidad positivo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "negativo": 0.15,
                "neutral": 0.25,
                "positivo": 0.60
            }
        }


class CommentFeatures(BaseModel):
    """Características extraídas del comentario"""
    emoji_score: float = Field(default=0, description="Score de emoticones")
    pos_word_score: float = Field(default=0, description="Score palabras positivas")
    neg_word_score: float = Field(default=0, description="Score palabras negativas")
    word_count: int = Field(default=0, description="Cantidad de palabras")
    
    class Config:
        json_schema_extra = {
            "example": {
                "emoji_score": 4.0,
                "pos_word_score": 12.0,
                "neg_word_score": 0.0,
                "word_count": 8
            }
        }


class SentimentAnalysisResponse(BaseModel):
    """Response de análisis de sentimiento individual"""
    comment: str = Field(..., description="Comentario analizado")
    sentiment: SentimentType = Field(..., description="Sentimiento detectado")
    confidence: float = Field(..., ge=0, le=1, description="Nivel de confianza")
    confidence_level: ConfidenceLevel = Field(..., description="Nivel de confianza categorizado")
    probabilities: SentimentProbabilities = Field(..., description="Probabilidades por clase")
    features: CommentFeatures = Field(..., description="Características extraídas")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp del análisis")
    
    @validator('confidence_level', pre=True, always=True)
    def set_confidence_level(cls, v, values):
        confidence = values.get('confidence', 0)
        if confidence >= 0.8:
            return ConfidenceLevel.HIGH
        elif confidence >= 0.6:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    class Config:
        json_schema_extra = {
            "example": {
                "comment": "La universidad tiene excelentes profesores",
                "sentiment": "Positivo",
                "confidence": 0.89,
                "confidence_level": "Alta",
                "probabilities": {
                    "negativo": 0.05,
                    "neutral": 0.06,
                    "positivo": 0.89
                },
                "features": {
                    "emoji_score": 0.0,
                    "pos_word_score": 12.0,
                    "neg_word_score": 0.0,
                    "word_count": 5
                },
                "timestamp": "2025-12-20T10:30:00"
            }
        }


class BatchAnalysisResponse(BaseModel):
    """Response de análisis por lote"""
    results: List[SentimentAnalysisResponse] = Field(..., description="Resultados individuales")
    summary: Dict[str, Any] = Field(..., description="Resumen estadístico")
    total_analyzed: int = Field(..., description="Total de comentarios analizados")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "results": [
                    {
                        "comment": "Excelente universidad",
                        "sentiment": "Positivo",
                        "confidence": 0.92,
                        "confidence_level": "Alta",
                        "probabilities": {
                            "negativo": 0.02,
                            "neutral": 0.06,
                            "positivo": 0.92
                        },
                        "features": {
                            "emoji_score": 0.0,
                            "pos_word_score": 15.0,
                            "neg_word_score": 0.0,
                            "word_count": 2
                        },
                        "timestamp": "2025-12-20T10:30:00"
                    }
                ],
                "summary": {
                    "sentiment_distribution": {
                        "Positivo": 5,
                        "Neutral": 2,
                        "Negativo": 3
                    },
                    "avg_confidence": 0.82
                },
                "total_analyzed": 10,
                "timestamp": "2025-12-20T10:30:00"
            }
        }


class StatisticsResponse(BaseModel):
    """Response de estadísticas del dataset"""
    total_comments: int = Field(..., description="Total de comentarios")
    distribution: Dict[str, int] = Field(..., description="Distribución por sentimiento")
    avg_comment_length: float = Field(..., description="Longitud promedio de comentarios")
    most_common_words: List[tuple] = Field(default=[], description="Palabras más comunes")
    model_info: Optional[Dict[str, Any]] = Field(None, description="Información del modelo")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_comments": 868,
                "distribution": {
                    "Positivo": 456,
                    "Neutral": 234,
                    "Negativo": 178
                },
                "avg_comment_length": 87.5,
                "most_common_words": [
                    ["universidad", 145],
                    ["excelente", 89],
                    ["profesores", 76]
                ],
                "model_info": {
                    "accuracy": 0.82,
                    "f1_weighted": 0.81,
                    "version": "3.0"
                },
                "timestamp": "2025-12-20T10:30:00"
            }
        }


class DatasetInfo(BaseModel):
    """Información del dataset cargado"""
    total_records: int = Field(..., description="Total de registros")
    columns: List[str] = Field(..., description="Columnas del dataset")
    sentiment_distribution: Dict[str, int] = Field(..., description="Distribución de sentimientos")
    date_loaded: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_records": 868,
                "columns": ["Comment", "Rating"],
                "sentiment_distribution": {
                    "Positivo": 456,
                    "Neutral": 234,
                    "Negativo": 178
                },
                "date_loaded": "2025-12-20T10:30:00"
            }
        }


class ModelTrainingResponse(BaseModel):
    """Response del entrenamiento del modelo"""
    status: str = Field(..., description="Estado del entrenamiento")
    accuracy: float = Field(..., description="Accuracy del modelo")
    f1_weighted: float = Field(..., description="F1-score ponderado")
    train_size: int = Field(..., description="Tamaño del set de entrenamiento")
    test_size: int = Field(..., description="Tamaño del set de prueba")
    features: int = Field(..., description="Número de características")
    training_date: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "completed",
                "accuracy": 0.82,
                "f1_weighted": 0.81,
                "train_size": 694,
                "test_size": 174,
                "features": 234,
                "training_date": "2025-12-20T10:30:00"
            }
        }


class ReportRequest(BaseModel):
    """Request para generar reporte"""
    period: str = Field(
        default="current",
        description="Periodo del reporte",
        example="current"
    )
    format: str = Field(
        default="json",
        description="Formato del reporte (json, pdf, xlsx)",
        example="json"
    )
    
    @validator('format')
    def validate_format(cls, v):
        allowed_formats = ['json', 'pdf', 'xlsx']
        if v not in allowed_formats:
            raise ValueError(f"Formato debe ser uno de: {allowed_formats}")
        return v


class ReportResponse(BaseModel):
    """Response de generación de reporte"""
    title: str = Field(..., description="Título del reporte")
    period: str = Field(..., description="Periodo analizado")
    summary: Dict[str, Any] = Field(..., description="Resumen ejecutivo")
    statistics: Dict[str, Any] = Field(..., description="Estadísticas detalladas")
    insights: List[str] = Field(default=[], description="Insights principales")
    recommendations: List[str] = Field(default=[], description="Recomendaciones")
    generated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Reporte de Análisis de Sentimientos UNMSM",
                "period": "Diciembre 2025",
                "summary": {
                    "total_comments": 868,
                    "positive_percentage": 52.5,
                    "engagement_rate": 8.4
                },
                "statistics": {
                    "sentiment_distribution": {
                        "Positivo": 456,
                        "Neutral": 234,
                        "Negativo": 178
                    }
                },
                "insights": [
                    "Tendencia positiva en últimas 3 semanas",
                    "Mayor engagement en publicaciones académicas"
                ],
                "recommendations": [
                    "Mantener comunicación de logros",
                    "Atender quejas recurrentes sobre trámites"
                ],
                "generated_at": "2025-12-20T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """Response de error estándar"""
    error: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje de error")
    detail: Optional[str] = Field(None, description="Detalle adicional")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "El comentario no puede estar vacío",
                "detail": "comment: field required",
                "timestamp": "2025-12-20T10:30:00"
            }
        }


class HealthCheckResponse(BaseModel):
    """Response de health check"""
    status: str = Field(..., description="Estado del sistema")
    timestamp: datetime = Field(default_factory=datetime.now)
    components: Dict[str, str] = Field(..., description="Estado de componentes")
    dataset_size: Optional[int] = Field(None, description="Tamaño del dataset")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-12-20T10:30:00",
                "components": {
                    "api": "online",
                    "analyzer": "online",
                    "dataset": "loaded",
                    "model": "loaded"
                },
                "dataset_size": 868
            }
        }
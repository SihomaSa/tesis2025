"""
Schemas para análisis de sentimientos - CORREGIDO
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SentimentLabel(str, Enum):
    """Etiquetas de sentimiento"""
    NEGATIVO = "Negativo"
    NEUTRAL = "Neutral"
    POSITIVO = "Positivo"

class SentimentProbabilities(BaseModel):
    """Probabilidades para cada clase de sentimiento"""
    negativo: float = Field(..., ge=0, le=1)
    neutral: float = Field(..., ge=0, le=1)
    positivo: float = Field(..., ge=0, le=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "negativo": 0.1,
                "neutral": 0.2,
                "positivo": 0.7
            }
        }

class CommentFeatures(BaseModel):
    """Características extraídas de un comentario"""
    emoji_score: float = Field(default=0)
    pos_word_score: float = Field(default=0)
    neg_word_score: float = Field(default=0)
    word_count: int = Field(default=0)
    char_count: int = Field(default=0)
    avg_word_length: float = Field(default=0)
    sentiment_diff: float = Field(default=0)
    
    # Conversión automática de features del modelo
    @classmethod
    def from_dict(cls, features: Dict[str, Any]) -> "CommentFeatures":
        """Crea CommentFeatures desde el diccionario del modelo"""
        return cls(
            emoji_score=float(features.get('emoji_score', 0)),
            pos_word_score=float(features.get('pos_word_score', 0)),
            neg_word_score=float(features.get('neg_word_score', 0)),
            word_count=int(features.get('word_count', 0)),
            char_count=int(features.get('char_count', 0)),
            avg_word_length=float(features.get('avg_word_len', 0)),
            sentiment_diff=float(features.get('sentiment_diff', 0))
        )

class CommentAnalysisRequest(BaseModel):
    """Request para análisis de un solo comentario"""
    text: str = Field(..., min_length=1, max_length=2000, description="Texto del comentario")
    include_details: bool = Field(True, description="Incluir detalles del análisis")
    include_suggestions: bool = Field(True, description="Incluir sugerencias")
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("El texto no puede estar vacío")
        return v.strip()

class SentimentAnalysisResponse(BaseModel):
    """Response para análisis de sentimiento"""
    success: bool = Field(True)
    comment: str
    sentiment: str
    confidence: float = Field(..., ge=0, le=1)
    confidence_level: str = Field("Media")
    probabilities: Optional[SentimentProbabilities] = None
    features: Optional[CommentFeatures] = None
    timestamp: Optional[str] = None
    error: Optional[str] = None
    
    @validator('confidence_level', pre=True, always=True)
    def set_confidence_level(cls, v, values):
        """Determina el nivel de confianza automáticamente"""
        confidence = values.get('confidence', 0)
        if confidence >= 0.75:
            return "Alta"
        elif confidence >= 0.50:
            return "Media"
        else:
            return "Baja"
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "comment": "La UNMSM tiene excelentes profesores",
                "sentiment": "Positivo",
                "confidence": 0.85,
                "confidence_level": "Alta",
                "probabilities": {
                    "negativo": 0.05,
                    "neutral": 0.10,
                    "positivo": 0.85
                },
                "features": {
                    "emoji_score": 0.0,
                    "pos_word_score": 15.0,
                    "neg_word_score": 0.0,
                    "word_count": 5
                },
                "timestamp": "2025-12-22T19:30:00"
            }
        }

class BatchAnalysisRequest(BaseModel):
    """Request para análisis por lotes"""
    texts: List[str] = Field(..., min_items=1, max_items=1000)
    batch_size: int = Field(100, ge=1, le=1000)
    include_details: bool = Field(True)
    
    @validator('texts')
    def validate_texts(cls, v):
        if not v:
            raise ValueError("La lista no puede estar vacía")
        return [t.strip() for t in v if t and t.strip()]

class BatchAnalysisResponse(BaseModel):
    """Response para análisis por lotes"""
    results: List[SentimentAnalysisResponse]
    summary: Dict[str, Any]
    total_analyzed: int
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    class Config:
        json_schema_extra = {
            "example": {
                "results": [],
                "summary": {
                    "sentiment_distribution": {
                        "Positivo": 5,
                        "Neutral": 2,
                        "Negativo": 3
                    },
                    "avg_confidence": 0.78
                },
                "total_analyzed": 10,
                "timestamp": "2025-12-22T19:30:00"
            }
        }

class StatisticsResponse(BaseModel):
    """Response de estadísticas"""
    total_comments: int
    distribution: Dict[str, int]
    avg_comment_length: float
    most_common_words: List[tuple]
    model_info: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class DatasetInfo(BaseModel):
    """Información del dataset"""
    total_records: int
    columns: List[str]
    sentiment_distribution: Dict[str, int]
    date_loaded: Optional[datetime] = None

class ModelTrainingResponse(BaseModel):
    """Response del entrenamiento"""
    status: str
    accuracy: float
    f1_weighted: float
    train_size: int
    test_size: int
    features: int
    training_date: str

class ReportRequest(BaseModel):
    """Request para reporte"""
    period: str = Field(default="current")
    format: str = Field(default="json")

class ReportResponse(BaseModel):
    """Response de reporte"""
    title: str
    period: str
    summary: Dict[str, Any]
    statistics: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    generated_at: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    """Response de error"""
    error: str
    message: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthCheckResponse(BaseModel):
    """Response de health check"""
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    components: Dict[str, str]
    dataset_size: Optional[int] = None
class SentimentResult(BaseModel):
    """Resultado de análisis de sentimiento (alias para compatibilidad)"""
    success: bool = Field(True)
    comment: str
    sentiment: str
    confidence: float = Field(..., ge=0, le=1)
    confidence_level: str = Field("Media")
    probabilities: Optional[SentimentProbabilities] = None
    features: Optional[CommentFeatures] = None
    timestamp: Optional[str] = None
    error: Optional[str] = None
    
    @validator('confidence_level', pre=True, always=True)
    def set_confidence_level(cls, v, values):
        """Determina el nivel de confianza automáticamente"""
        confidence = values.get('confidence', 0)
        if confidence >= 0.75:
            return "Alta"
        elif confidence >= 0.50:
            return "Media"
        else:
            return "Baja"
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "comment": "La UNMSM tiene excelentes profesores",
                "sentiment": "Positivo",
                "confidence": 0.85,
                "confidence_level": "Alta"
            }
        }
# Aliases para compatibilidad
CommentAnalysisResponse = SentimentAnalysisResponse
SentimentAnalysisRequest = CommentAnalysisRequest
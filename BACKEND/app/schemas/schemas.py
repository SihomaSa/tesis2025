"""
Esquemas Pydantic para la API - Versión mejorada
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# Esquema para respuesta de análisis
class SentimentAnalysisResponse(BaseModel):
    comment: str
    sentiment: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    probabilities: Dict[str, float]
    features: Optional[Dict[str, Any]] = None
    timestamp: datetime

# Esquema para batch analysis
class BatchAnalysisResponse(BaseModel):
    results: List[SentimentAnalysisResponse]
    total_comments: int
    processing_time: float
    timestamp: datetime

# Esquema para estadísticas
class StatisticsResponse(BaseModel):
    total_comments: int
    distribution: Dict[str, int]
    percentages: Optional[Dict[str, float]] = None
    avg_comment_length: float
    most_common_words: List[tuple]
    model_info: Optional[Dict[str, Any]] = None
    dataset_sample_size: Optional[int] = None
    timestamp: datetime

# Esquema para análisis por temas
class TopicAnalysisResponse(BaseModel):
    name: str
    positive: int
    neutral: int
    negative: int
    total: int
    percentage: Optional[float] = None

# Esquema para comentario reciente
class RecentCommentResponse(BaseModel):
    comment: str
    sentiment: str
    confidence: float
    timestamp: Optional[datetime] = None

# Esquema para datos del dashboard
class DashboardDataResponse(BaseModel):
    metrics: Dict[str, Any]
    topics_analysis: List[TopicAnalysisResponse]
    recent_comments: List[RecentCommentResponse]
    model_info: Optional[Dict[str, Any]]
    timestamp: datetime

# Esquema para dataset info
class DatasetInfoResponse(BaseModel):
    total_comments: int
    distribution: Dict[str, int]
    percentages: Dict[str, float]
    sample_comments: List[Dict[str, Any]]
    columns: List[str]
    timestamp: datetime

# Esquema para error
class ErrorResponse(BaseModel):
    error: str
    message: str
    detail: Optional[str] = None
    timestamp: datetime
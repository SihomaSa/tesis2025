"""
SCHEMAS DE REPORTES - API UNMSM
✅ Modelos Pydantic para reportes ejecutivos
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime


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


class ReportStatistics(BaseModel):
    """Estadísticas detalladas"""
    sentiment_distribution: Dict[str, int]
    avg_comment_length: float = Field(..., ge=0)
    total_words: int = Field(..., ge=0)
    unique_words: int = Field(..., ge=0)
    most_common_words: List[tuple] = Field(default_factory=list)


class CategoryScore(BaseModel):
    """Score por categoría"""
    name: str
    score: int = Field(..., ge=0, le=100)
    description: str
    positive_count: int = Field(..., ge=0)
    neutral_count: int = Field(..., ge=0)
    negative_count: int = Field(..., ge=0)
    total_count: int = Field(..., ge=0)


class ReportInsight(BaseModel):
    """Insight del reporte"""
    type: Literal["positive", "warning", "info", "critical"]
    title: str
    description: str
    metric: float
    icon: str = "ℹ"


class ReportRecommendation(BaseModel):
    """Recomendación del reporte"""
    category: Literal["potenciar", "mejorar", "monitorear", "urgente"]
    title: str
    items: List[str]
    priority: Literal["high", "medium", "low"]


class WordTag(BaseModel):
    """Palabra para nube de palabras"""
    text: str
    size: int = Field(..., ge=10, le=40)
    count: int = Field(..., ge=1)


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
    
    model_config = ConfigDict(from_attributes=True)


class PeriodOption(BaseModel):
    """Opción de período"""
    value: str
    label: str
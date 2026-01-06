# """
# Schemas para la API - UNMSM Sentiment Analysis
# """

# from .analysis import (
#     CommentAnalysisRequest,
#     CommentAnalysisResponse,
#     SentimentAnalysisRequest,
#     SentimentAnalysisResponse,
#     BatchAnalysisRequest,
#     BatchAnalysisResponse,
#     ReportRequest,
#     ReportResponse,
#     SentimentResult,
#     SentimentProbabilities,
#     CommentFeatures,
#     DatasetInfo,
#     ModelTrainingResponse,
#     StatisticsResponse,
#     ModelInfo,
#     HealthCheck,
#     ErrorResponse
# )

# __all__ = [
#     "CommentAnalysisRequest",
#     "CommentAnalysisResponse",
#     "SentimentAnalysisRequest",
#     "SentimentAnalysisResponse",
#     "BatchAnalysisRequest",
#     "BatchAnalysisResponse",
#     "ReportRequest",
#     "ReportResponse",
#     "SentimentResult",
#     "SentimentProbabilities",
#     "CommentFeatures",
#     "DatasetInfo",
#     "ModelTrainingResponse",
#     "StatisticsResponse",
#     "ModelInfo",
#     "HealthCheck",
#     "ErrorResponse"
# ]
# app/schemas/__init__.py
"""
Schemas para la API - UNMSM Sentiment Analysis
✅ Exportaciones corregidas para reportes
"""

from .analysis import (
    CommentAnalysisRequest,
    SentimentAnalysisResponse,
    BatchAnalysisRequest,
    BatchAnalysisResponse,
    SentimentProbabilities,
    CommentFeatures,
    DatasetInfo,
    ModelTrainingResponse,
    StatisticsResponse,
    HealthCheckResponse,
    SentimentResult,
    ErrorResponse
)

# ✅ NUEVOS IMPORTS PARA REPORTES
from .reports import (
    ReportRequest,
    ReportResponse,
    ReportSummary,
    ReportStatistics,
    ReportInsight,
    ReportRecommendation,
    CategoryScore,
    WordTag,
    PeriodOption
)

__all__ = [
    # Análisis
    "CommentAnalysisRequest",
    "SentimentAnalysisResponse",
    "BatchAnalysisRequest",
    "BatchAnalysisResponse",
    "SentimentProbabilities",
    "CommentFeatures",
    "DatasetInfo",
    "ModelTrainingResponse",
    "StatisticsResponse",
    "HealthCheckResponse",
    "SentimentResult",
    "ErrorResponse",
    
    # ✅ Reportes
    "ReportRequest",
    "ReportResponse",
    "ReportSummary",
    "ReportStatistics",
    "ReportInsight",
    "ReportRecommendation",
    "CategoryScore",
    "WordTag",
    "PeriodOption"
]
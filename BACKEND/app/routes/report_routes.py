"""
RUTAS DE REPORTES - API UNMSM
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

from app.schemas import ReportRequest, ReportResponse, ErrorResponse
from app.core.dependencies import get_sentiment_analyzer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/generate",
    response_model=ReportResponse,
    summary="Generar reporte",
    description="Genera un reporte completo de análisis de sentimientos"
)
async def generate_report(
    request: ReportRequest,
    analyzer=Depends(get_sentiment_analyzer)
):
    """
    Genera un reporte ejecutivo completo.
    
    **Parámetros:**
    - **period**: Periodo del reporte (default: "current")
    - **format**: Formato de salida (json, pdf, xlsx)
    """
    try:
        logger.info(f"📄 Generando reporte - Periodo: {request.period}, Formato: {request.format}")
        
        # Obtener estadísticas
        stats = analyzer.get_statistics()
        
        if 'error' in stats:
            raise HTTPException(status_code=404, detail=stats['error'])
        
        # Calcular métricas
        distribution = stats['distribution']
        total = stats['total_comments']
        
        positive_pct = (distribution.get('Positivo', 0) / total * 100) if total > 0 else 0
        negative_pct = (distribution.get('Negativo', 0) / total * 100) if total > 0 else 0
        neutral_pct = (distribution.get('Neutral', 0) / total * 100) if total > 0 else 0
        
        # Determinar percepción general
        if positive_pct > negative_pct and positive_pct > neutral_pct:
            general_perception = "positiva"
        elif negative_pct > positive_pct:
            general_perception = "negativa"
        else:
            general_perception = "neutral"
        
        # Generar insights
        insights = []
        
        if positive_pct > 60:
            insights.append(f"Percepción predominantemente positiva ({positive_pct:.1f}%)")
        
        if negative_pct > 30:
            insights.append(f"Se identifican áreas críticas de mejora ({negative_pct:.1f}% negativos)")
        
        if positive_pct > negative_pct * 2:
            insights.append("Tendencia favorable: comentarios positivos duplican los negativos")
        
        if len(stats.get('most_common_words', [])) > 0:
            top_word = stats['most_common_words'][0][0]
            insights.append(f"Término más mencionado: '{top_word}'")
        
        # Generar recomendaciones
        recommendations = [
            "Monitorear continuamente los comentarios en redes sociales",
            "Atender las quejas recurrentes identificadas",
            "Fortalecer la comunicación de logros y mejoras"
        ]
        
        if negative_pct > 25:
            recommendations.append("PRIORITARIO: Implementar plan de acción para áreas críticas")
        
        if general_perception == "positiva":
            recommendations.append("Mantener estrategias actuales de comunicación")
        else:
            recommendations.append("Revisar estrategia de comunicación institucional")
        
        # Construir reporte
        report = ReportResponse(
            title="Reporte de Análisis de Sentimientos - UNMSM",
            period=f"Diciembre 2025" if request.period == "current" else request.period,
            summary={
                "total_comments": total,
                "positive_percentage": round(positive_pct, 1),
                "negative_percentage": round(negative_pct, 1),
                "neutral_percentage": round(neutral_pct, 1),
                "general_perception": general_perception,
                "engagement_rate": round(positive_pct * 0.15, 1),
                "model_confidence": stats.get('model', {}).get('accuracy', 0)
            },
            statistics={
                "sentiment_distribution": distribution,
                "avg_comment_length": round(stats['avg_comment_length'], 1),
                "most_common_words": stats.get('most_common_words', [])[:10]
            },
            insights=insights,
            recommendations=recommendations,
            generated_at=datetime.now()
        )
        
        logger.info(f"✅ Reporte generado exitosamente")
        
        # Si el formato no es JSON, podrías generar PDF/XLSX aquí
        if request.format != "json":
            logger.warning(f"⚠️  Formato {request.format} no implementado aún, retornando JSON")
        
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error generando reporte: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando reporte: {str(e)}"
        )


@router.get(
    "/latest",
    summary="Último reporte",
    description="Obtiene el último reporte generado (simulado)"
)
async def get_latest_report(analyzer=Depends(get_sentiment_analyzer)):
    """Obtiene el último reporte generado"""
    # En producción, esto obtendría el reporte de una base de datos
    request = ReportRequest(period="current", format="json")
    return await generate_report(request, analyzer)
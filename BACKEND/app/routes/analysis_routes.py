"""
RUTAS DE ANÁLISIS - API UNMSM - CORREGIDO
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging
from datetime import datetime
from app.schemas import (
    CommentAnalysisRequest,
    BatchAnalysisRequest,
    SentimentAnalysisResponse,
    BatchAnalysisResponse,
    SentimentProbabilities,
    CommentFeatures,
    ErrorResponse
)
from app.core.dependencies import get_sentiment_analyzer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/single",
    response_model=SentimentAnalysisResponse,
    summary="Analizar comentario individual",
    description="Analiza el sentimiento de un comentario individual"
)
async def analyze_single_comment(
    request: CommentAnalysisRequest,
    analyzer=Depends(get_sentiment_analyzer)
):
    """
    Analiza un comentario individual y retorna el sentimiento detectado.
    """
    try:
        logger.info(f"📝 Analizando: {request.text[:50]}...")
        
        # Analizar usando el texto del request
        result = analyzer.analyze_single(request.text)
        
        logger.info(f"🔍 Resultado raw del modelo: {result}")
        
        # Convertir features usando el método from_dict
        features = CommentFeatures.from_dict(result.get('features', {}))
        
        # Construir response
        response = SentimentAnalysisResponse(
            success=True,
            comment=result['comment'],
            sentiment=result['sentiment'],
            confidence=result['confidence'],
            probabilities=SentimentProbabilities(
                negativo=result['probabilities']['negativo'],
                neutral=result['probabilities']['neutral'],
                positivo=result['probabilities']['positivo']
            ),
            features=features,
            timestamp=result.get('timestamp', datetime.now().isoformat())
        )
        
        logger.info(f"✅ Análisis: {response.sentiment} ({response.confidence:.2%})")
        logger.info(f"📊 Probs: N={response.probabilities.negativo:.2f} "
                   f"Ne={response.probabilities.neutral:.2f} "
                   f"P={response.probabilities.positivo:.2f}")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en análisis: {e}", exc_info=True)
        return SentimentAnalysisResponse(
            success=False,
            comment=request.text,
            sentiment="Error",
            confidence=0.0,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )


@router.post(
    "/batch",
    response_model=BatchAnalysisResponse,
    summary="Analizar múltiples comentarios"
)
async def analyze_batch_comments(
    request: BatchAnalysisRequest,
    analyzer=Depends(get_sentiment_analyzer)
):
    """
    Analiza múltiples comentarios en un solo request.
    """
    try:
        logger.info(f"📦 Analizando lote de {len(request.texts)} comentarios...")
        
        # Analizar batch
        raw_results = analyzer.analyze_batch(request.texts)
        
        # Construir responses
        results = []
        sentiment_counts = {'Positivo': 0, 'Neutral': 0, 'Negativo': 0}
        total_confidence = 0
        
        for i, raw_result in enumerate(raw_results):
            if 'error' in raw_result:
                logger.warning(f"⚠️  Error en comentario {i}: {raw_result.get('error')}")
                continue
            
            features = CommentFeatures.from_dict(raw_result.get('features', {}))
            
            result = SentimentAnalysisResponse(
                success=True,
                comment=request.texts[i],
                sentiment=raw_result['sentiment'],
                confidence=raw_result['confidence'],
                probabilities=SentimentProbabilities(**raw_result['probabilities']),
                features=features,
                timestamp=raw_result.get('timestamp', datetime.now().isoformat())
            )
            
            results.append(result)
            sentiment_counts[raw_result['sentiment']] += 1
            total_confidence += raw_result['confidence']
        
        # Resumen
        total = len(results)
        avg_confidence = total_confidence / total if total > 0 else 0
        
        summary = {
            'sentiment_distribution': sentiment_counts,
            'avg_confidence': round(avg_confidence, 3),
            'positive_percentage': round((sentiment_counts['Positivo'] / total * 100), 1) if total > 0 else 0,
            'negative_percentage': round((sentiment_counts['Negativo'] / total * 100), 1) if total > 0 else 0,
            'neutral_percentage': round((sentiment_counts['Neutral'] / total * 100), 1) if total > 0 else 0
        }
        
        response = BatchAnalysisResponse(
            results=results,
            summary=summary,
            total_analyzed=total,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"✅ Batch completado: {total} comentarios")
        logger.info(f"📊 Distribución: {sentiment_counts}")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en batch: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test", summary="Endpoint de prueba")
async def test_analysis(analyzer=Depends(get_sentiment_analyzer)):
    """
    Endpoint de prueba con comentarios predefinidos.
    """
    test_comments = [
        "La UNMSM tiene excelentes profesores y muy buena infraestructura",
        "Excelente universidad, me encanta estudiar aquí",
        "Pésimo servicio en la administración, siempre hay problemas",
        "La biblioteca es regular, nada especial",
        "Me encanta esta universidad, los profesores son geniales 🎓❤️"
    ]
    
    try:
        results = analyzer.analyze_batch(test_comments)
        
        return {
            "message": "Test ejecutado exitosamente",
            "results": results,
            "total": len(results),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error en test: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/predict",
    response_model=SentimentAnalysisResponse,
    summary="Predicción rápida"
)
async def predict_sentiment(
    request: CommentAnalysisRequest,
    analyzer=Depends(get_sentiment_analyzer)
):
    """
    Predicción rápida de sentimiento (alias de /single).
    """
    return await analyze_single_comment(request, analyzer)
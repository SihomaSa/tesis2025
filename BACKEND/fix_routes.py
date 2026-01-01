import os

print("=== CORRIGIENDO RUTAS DE ANÁLISIS ===")

# Contenido corregido para analysis_routes.py
analysis_routes_content = '''
"""
RUTAS DE ANÁLISIS - API UNMSM - SIMPLIFICADO Y FUNCIONAL
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging
from datetime import datetime
from app.core.dependencies import get_sentiment_analyzer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/single",
    summary="Analizar comentario individual",
    description="Analiza el sentimiento de un comentario individual"
)
async def analyze_single_comment(
    text: str,
    include_details: bool = True,
    include_suggestions: bool = False,
    analyzer = Depends(get_sentiment_analyzer)
):
    """
    Analiza un comentario individual y retorna el sentimiento detectado.
    """
    try:
        logger.info(f"📝 Analizando: {text[:50]}...")
        
        # Analizar usando el método analyze_single
        result = analyzer.analyze_single(text)
        
        # Construir response
        response = {
            "success": "error" not in result and result.get('sentimiento') != 'Error',
            "comment": result.get('comment', text),
            "sentiment": result.get('sentimiento', 'Error'),
            "confidence": result.get('confianza', 0.0),
            "confidence_level": "Alta" if result.get('confianza', 0) > 0.7 else 
                              "Media" if result.get('confianza', 0) > 0.4 else "Baja",
            "probabilities": result.get('probabilities', {
                "negativo": 0.0,
                "neutral": 0.0,
                "positivo": 0.0
            }),
            "features": result.get('features', {}),
            "timestamp": result.get('timestamp', datetime.now().isoformat())
        }
        
        if "error" in result:
            response["error"] = result["error"]
        
        logger.info(f"✅ Análisis: {response['sentiment']} ({response['confidence']:.2%})")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en análisis: {e}", exc_info=True)
        return {
            "success": False,
            "comment": text,
            "sentiment": "Error",
            "confidence": 0.0,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@router.post(
    "/batch",
    summary="Analizar múltiples comentarios"
)
async def analyze_batch_comments(
    texts: List[str],
    batch_size: int = 100,
    include_details: bool = True,
    analyzer = Depends(get_sentiment_analyzer)
):
    """
    Analiza múltiples comentarios en un solo request.
    """
    try:
        logger.info(f"📦 Analizando lote de {len(texts)} comentarios...")
        
        # Analizar batch
        results = analyzer.analyze_batch(texts)
        
        # Calcular estadísticas
        sentiment_counts = {"Positivo": 0, "Neutral": 0, "Negativo": 0, "Error": 0}
        total_confidence = 0
        successful = 0
        
        processed_results = []
        for i, result in enumerate(results):
            if "error" in result or result.get("sentimiento") == "Error":
                sentiment_counts["Error"] += 1
                processed_result = {
                    "comment": texts[i] if i < len(texts) else "Unknown",
                    "sentiment": "Error",
                    "confidence": 0.0,
                    "error": result.get("error", "Unknown error")
                }
            else:
                sentiment = result.get("sentimiento", "Neutral")
                sentiment_counts[sentiment] += 1
                total_confidence += result.get("confianza", 0.0)
                successful += 1
                
                processed_result = {
                    "comment": result.get("comment", texts[i]),
                    "sentiment": sentiment,
                    "confidence": result.get("confianza", 0.0),
                    "probabilities": result.get("probabilities", {}),
                    "features": result.get("features", {}) if include_details else None
                }
            
            processed_results.append(processed_result)
        
        # Resumen
        avg_confidence = total_confidence / successful if successful > 0 else 0
        
        response = {
            "results": processed_results,
            "summary": {
                "total_analyzed": len(texts),
                "successful_analysis": successful,
                "failed_analysis": len(texts) - successful,
                "avg_confidence": round(avg_confidence, 3),
                "sentiment_distribution": sentiment_counts
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ Batch completado: {successful}/{len(texts)} exitosos")
        
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
            "comments": test_comments,
            "results": results,
            "total": len(results),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error en test: {e}")
        return {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@router.post(
    "/predict",
    summary="Predicción rápida"
)
async def predict_sentiment(
    text: str,
    include_details: bool = True,
    include_suggestions: bool = False,
    analyzer = Depends(get_sentiment_analyzer)
):
    """
    Predicción rápida de sentimiento (alias de /single).
    """
    return await analyze_single_comment(text, include_details, include_suggestions, analyzer)
'''

# Guardar el archivo de rutas corregido
with open('app/routes/analysis_routes.py', 'w', encoding='utf-8') as f:
    f.write(analysis_routes_content)

print("✅ analysis_routes.py actualizado")

print("\n✅ CORRECCIONES APLICADAS:")
print("1. sentiment_analyzer.py ahora tiene analyze_single() y analyze_batch()")
print("2. analysis_routes.py simplificado para usar los métodos correctos")
print("3. Ambas partes ahora son compatibles")
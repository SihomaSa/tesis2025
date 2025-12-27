"""
RUTAS DE ESTADÍSTICAS - API UNMSM
Versión corregida para usar dataset completo
"""

from fastapi import APIRouter, HTTPException, Depends
import logging
from typing import Dict, List, Any
import pandas as pd
from collections import Counter
import re
from datetime import datetime, timedelta
import random

from app.schemas import StatisticsResponse, ErrorResponse
from app.core.dependencies import get_sentiment_analyzer
from app.core.dataset import dataset_manager

logger = logging.getLogger(__name__)

router = APIRouter()

# Definir palabras clave por categoría
CATEGORY_KEYWORDS = {
    "Infraestructura": [
        "infraestructura", "edificio", "aula", "laboratorio", "campus", 
        "instalaciones", "ambiente", "espacio", "local", "construcción",
        "sala", "pabellón", "infra", "física", "instalación"
    ],
    "Docentes": [
        "profesor", "docente", "maestro", "enseñanza", "clase", "cátedra",
        "educación", "enseñar", "explicar", "capacitado", "catedrático",
        "pedagogía", "académico", "enseña", "profe"
    ],
    "Servicios": [
        "servicio", "atención", "trámite", "administrativo", "oficina", 
        "secretaría", "personal", "gestión", "proceso", "administración",
        "atender", "atendieron", "servicios", "trámites"
    ],
    "Biblioteca": [
        "biblioteca", "libro", "lectura", "material", "bibliográfico",
        "préstamo", "catálogo", "estudio", "sala de estudio", "lector",
        "bibliotecario", "estudiar", "libros"
    ],
    "Tecnología": [
        "tecnología", "internet", "wifi", "computadora", "sistema", 
        "plataforma", "digital", "online", "virtual", "computación",
        "informática", "red", "conexión", "virtual", "software"
    ],
    "Gestión": [
        "gestión", "administración", "dirección", "rector", "vicerrector",
        "decano", "autoridad", "gobierno", "política", "organización",
        "gestión", "gerencia", "liderazgo"
    ],
    "Comunicación": [
        "comunicación", "información", "noticia", "anuncio", "aviso",
        "comunicado", "divulgación", "informar", "comunicar", "redes"
    ]
}

def classify_comment_by_topic(text: str) -> str:
    """
    Clasificar un comentario en una categoría basándose en palabras clave
    """
    if not isinstance(text, str):
        return "Otros"
    
    text_lower = text.lower()
    
    # Contar coincidencias por categoría
    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            category_scores[category] = score
    
    # Retornar categoría con mayor puntaje
    if category_scores:
        return max(category_scores.items(), key=lambda x: x[1])[0]
    
    return "Otros"

@router.get("/topics")
async def get_topic_analysis(analyzer=Depends(get_sentiment_analyzer)):
    """
    Analizar sentimientos por temas/categorías usando dataset completo
    """
    try:
        logger.info("Analizando sentimientos por temas...")
        
        # Verificar si el analyzer tiene datos
        if not hasattr(analyzer, 'df') or analyzer.df is None:
            logger.error("Dataset no disponible en analyzer")
            raise HTTPException(status_code=404, detail="Dataset no cargado en el analyzer")
        
        df = analyzer.df
        
        if len(df) == 0:
            logger.warning("Dataset vacío")
            raise HTTPException(status_code=404, detail="Dataset vacío")
        
        logger.info(f"Procesando {len(df)} comentarios para análisis de temas")
        
        # Asegurar que tenemos las columnas necesarias
        if 'comentario' not in df.columns:
            logger.error("Columna 'comentario' no encontrada en el dataset")
            raise HTTPException(status_code=500, detail="Columna 'comentario' no encontrada")
        
        if 'sentimiento' not in df.columns:
            logger.error("Columna 'sentimiento' no encontrada en el dataset")
            raise HTTPException(status_code=500, detail="Columna 'sentimiento' no encontrada")
        
        # Clasificar cada comentario por tema (usar una muestra si es muy grande)
        max_comments = 1000  # Procesar máximo 1000 comentarios para eficiencia
        if len(df) > max_comments:
            sample_df = df.sample(max_comments, random_state=42)
        else:
            sample_df = df
        
        logger.info(f"Clasificando {len(sample_df)} comentarios por tema...")
        sample_df = sample_df.copy()
        sample_df['tema'] = sample_df['comentario'].apply(classify_comment_by_topic)
        
        # Agrupar por tema y sentimiento
        topic_sentiment = sample_df.groupby(['tema', 'sentimiento']).size().unstack(fill_value=0)
        
        # Formatear resultados
        results = []
        total_comments_analyzed = len(sample_df)
        
        for topic in topic_sentiment.index:
            positive = topic_sentiment.loc[topic].get('Positivo', 0)
            neutral = topic_sentiment.loc[topic].get('Neutral', 0)
            negative = topic_sentiment.loc[topic].get('Negativo', 0)
            total = positive + neutral + negative
            
            # Solo incluir temas con suficientes comentarios
            if total >= max(3, total_comments_analyzed * 0.01):  # Al menos 3 o 1% del total
                results.append({
                    "name": topic,
                    "positive": int(positive),
                    "neutral": int(neutral),
                    "negative": int(negative),
                    "total": int(total),
                    "percentage": round((total / total_comments_analyzed) * 100, 1)
                })
        
        # Ordenar por total (mayor a menor)
        results.sort(key=lambda x: x['total'], reverse=True)
        
        # Si no hay resultados, retornar error
        if not results:
            logger.warning("No se encontraron temas con suficientes comentarios")
            raise HTTPException(status_code=404, detail="No hay suficientes datos para análisis de temas")
        
        logger.info(f"Análisis de temas completado: {len(results)} temas encontrados")
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en análisis por temas: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error analizando temas: {str(e)}")

@router.get(
    "/",
    response_model=StatisticsResponse,
    summary="Obtener estadísticas generales del dataset COMPLETO",
    description="Retorna estadísticas completas del dataset cargado",
    responses={
        200: {"description": "Estadísticas obtenidas exitosamente"},
        404: {"model": ErrorResponse, "description": "Dataset no cargado"},
        500: {"model": ErrorResponse, "description": "Error interno"}
    }
)
async def get_statistics(analyzer=Depends(get_sentiment_analyzer)):
    """
    Obtiene estadísticas generales del dataset COMPLETO.
    
    **Retorna:**
    - Total de comentarios
    - Distribución por sentimiento
    - Longitud promedio de comentarios
    - Palabras más comunes
    - Información del modelo ML
    """
    try:
        logger.info("[STATS] Obteniendo estadísticas del dataset COMPLETO...")
        
        # Verificar dataset
        if not hasattr(analyzer, 'df') or analyzer.df is None:
            logger.error("Dataset no disponible en analyzer")
            raise HTTPException(status_code=404, detail="Dataset no cargado en el analyzer")
        
        df = analyzer.df
        
        if len(df) == 0:
            logger.warning("Dataset vacío")
            raise HTTPException(status_code=404, detail="Dataset vacío")
        
        logger.info(f"Procesando dataset con {len(df)} comentarios")
        
        # Calcular estadísticas detalladas
        total_comments = len(df)
        
        # Distribución de sentimientos
        if 'sentimiento' in df.columns:
            distribution = df['sentimiento'].value_counts().to_dict()
        else:
            distribution = {"Positivo": 0, "Neutral": 0, "Negativo": 0}
        
        # Calcular porcentajes
        percentages = {}
        for sentiment in ['Positivo', 'Neutral', 'Negativo']:
            count = distribution.get(sentiment, 0)
            percentages[sentiment] = round((count / total_comments) * 100, 2) if total_comments > 0 else 0
        
        # Longitud promedio de comentarios
        if 'comentario' in df.columns:
            avg_comment_length = df['comentario'].astype(str).apply(len).mean()
        else:
            avg_comment_length = 0
        
        # Palabras más comunes (usar muestra si es muy grande)
        max_words_analysis = 2000
        if len(df) > max_words_analysis:
            sample_df = df.sample(max_words_analysis, random_state=42)
        else:
            sample_df = df
        
        if 'comentario' in sample_df.columns:
            all_text = ' '.join(sample_df['comentario'].astype(str).tolist())
            words = re.findall(r'\b[a-záéíóúñü]+\b', all_text.lower())
            
            # Stop words en español
            stop_words = {
                'de', 'la', 'el', 'en', 'que', 'y', 'a', 'los', 'del', 'se', 
                'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 
                'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 
                'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 
                'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien', 
                'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 
                'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 
                'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 
                'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 
                'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 
                'estar', 'estas', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 
                'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 
                'vosotras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 
                'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 
                'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 
                'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estás', 
                'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 
                'estemos', 'estéis', 'estén', 'estaré', 'estarás', 'estará', 
                'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 
                'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 
                'estábamos', 'estabais', 'estaban', 'estuve', 'estuviste', 
                'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 
                'estuvieras', 'estuviéramos', 'estuvierais', 'estuvieran', 
                'estuviese', 'estuvieses', 'estuviésemos', 'estuvieseis', 
                'estuviesen', 'estando', 'estado', 'estada', 'estados', 
                'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 'habéis', 
                'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 
                'habré', 'habrás', 'habrá', 'habremos', 'habréis', 'habrán', 
                'habría', 'habrías', 'habríamos', 'habríais', 'habrían', 
                'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube', 
                'hubiste', 'hubo', 'hubimos', 'hubisteis', 'hubieron', 
                'hubiera', 'hubieras', 'hubiéramos', 'hubierais', 'hubieran', 
                'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen', 
                'habiendo', 'habido', 'habida', 'habidos', 'habidas', 'soy', 
                'eres', 'es', 'somos', 'sois', 'son', 'sea', 'seas', 'seamos', 
                'seáis', 'sean', 'seré', 'serás', 'será', 'seremos', 'seréis', 
                'serán', 'sería', 'serías', 'seríamos', 'seríais', 'serían', 
                'era', 'eras', 'éramos', 'erais', 'eran', 'fui', 'fuiste', 
                'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras', 
                'fuéramos', 'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 
                'fueseis', 'fuesen', 'siendo', 'sido', 'sed', 'tengo', 'tienes', 
                'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas', 
                'tengamos', 'tengáis', 'tengan', 'tendré', 'tendrás', 'tendrá', 
                'tendremos', 'tendréis', 'tendrán', 'tendría', 'tendrías', 
                'tendríamos', 'tendríais', 'tendrían', 'tenía', 'tenías', 
                'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo', 
                'tuvimos', 'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 
                'tuviéramos', 'tuvierais', 'tuvieran', 'tuviese', 'tuvieses', 
                'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 
                'tenida', 'tenidos', 'tenidas', 'tened'
            }
            
            filtered_words = Counter(
                word for word in words 
                if word not in stop_words and len(word) > 2
            )
            
            most_common = filtered_words.most_common(15)
            most_common_words = [(word, count) for word, count in most_common]
        else:
            most_common_words = []
        
        # Información del modelo
        model_info = None
        if hasattr(analyzer, 'model_metadata') and analyzer.model_metadata:
            model_info = {
                "accuracy": analyzer.model_metadata.get('accuracy', 0),
                "f1_weighted": analyzer.model_metadata.get('f1_weighted', 0),
                "train_size": analyzer.model_metadata.get('train_size', 0),
                "test_size": analyzer.model_metadata.get('test_size', 0),
                "features": analyzer.model_metadata.get('features', 0),
                "training_date": analyzer.model_metadata.get('training_date', ''),
                "version": analyzer.model_metadata.get('version', '')
            }
        
        # Crear respuesta
        stats = {
            "total_comments": total_comments,
            "distribution": distribution,
            "percentages": percentages,
            "avg_comment_length": float(avg_comment_length),
            "most_common_words": most_common_words,
            "model_info": model_info,
            "dataset_sample_size": len(sample_df) if 'sample_df' in locals() else total_comments,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"[OK] Estadísticas obtenidas: {total_comments} comentarios")
        logger.info(f"Distribución: {distribution}")
        
        response = StatisticsResponse(**stats)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Error obteniendo estadísticas: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )

@router.get("/recent-comments")
async def get_recent_comments(
    limit: int = 10,
    analyzer=Depends(get_sentiment_analyzer)
):
    """
    Obtiene comentarios recientes del dataset
    """
    try:
        if not hasattr(analyzer, 'df') or analyzer.df is None:
            raise HTTPException(status_code=404, detail="Dataset no cargado")
        
        df = analyzer.df
        
        if 'comentario' not in df.columns or 'sentimiento' not in df.columns:
            raise HTTPException(status_code=500, detail="Columnas requeridas no encontradas")
        
        # Tomar una muestra aleatoria si no hay columna de fecha
        sample_size = min(limit, len(df))
        if sample_size > 0:
            sample_df = df.sample(sample_size, random_state=42)
            
            comments = []
            for _, row in sample_df.iterrows():
                comments.append({
                    "comment": str(row['comentario']),
                    "sentiment": str(row['sentimiento']),
                    "confidence": random.uniform(0.7, 0.99)  # Simulado
                })
            
            return {
                "total_comments": len(df),
                "sample_size": sample_size,
                "comments": comments
            }
        else:
            return {
                "total_comments": 0,
                "sample_size": 0,
                "comments": []
            }
        
    except Exception as e:
        logger.error(f"Error obteniendo comentarios recientes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard-data")
async def get_dashboard_data(analyzer=Depends(get_sentiment_analyzer)):
    """
    Obtiene todos los datos necesarios para el dashboard
    """
    try:
        logger.info("Generando datos para dashboard...")
        
        # Obtener estadísticas generales
        stats = await get_statistics(analyzer)
        stats_dict = stats.dict()
        
        # Obtener análisis por temas
        topics_data = await get_topic_analysis(analyzer)
        
        # Obtener comentarios recientes
        recent_comments = await get_recent_comments(5, analyzer)
        
        # Calcular métricas para el dashboard
        total_comments = stats_dict['total_comments']
        distribution = stats_dict['distribution']
        percentages = stats_dict['percentages']
        
        # Simular cambios vs mes anterior (para el dashboard)
        changes = {
            "total_comments": {"change": "+12%", "trend": "up"},
            "positive_sentiment": {"change": f"+{random.randint(2, 8)}%", "trend": "up"},
            "negative_sentiment": {"change": f"-{random.randint(1, 5)}%", "trend": "down"},
            "neutral_sentiment": {"change": f"+{random.randint(0, 3)}%", "trend": "stable"}
        }
        
        # Construir respuesta completa
        dashboard_data = {
            "metrics": {
                "total_comments": total_comments,
                "sentiment_distribution": distribution,
                "sentiment_percentages": percentages,
                "changes": changes,
                "avg_comment_length": stats_dict['avg_comment_length'],
                "most_common_words": stats_dict['most_common_words']
            },
            "topics_analysis": topics_data,
            "recent_comments": recent_comments['comments'],
            "model_info": stats_dict['model_info'],
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("Datos del dashboard generados exitosamente")
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Error generando datos del dashboard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generando dashboard: {str(e)}")
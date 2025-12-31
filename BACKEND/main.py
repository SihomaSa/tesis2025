"""
BACKEND PRINCIPAL - SISTEMA DE ANÁLISIS DE SENTIMIENTOS UNMSM
Versión: 3.2 - Usando dataset completo
"""

import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import logging
from datetime import datetime
from pathlib import Path
import sklearn.utils
if not hasattr(sklearn.utils, 'parse_version'):
    from pkg_resources import parse_version as parse_version_
    sklearn.utils.parse_version = parse_version_
    print("✅ Applied monkey patch for sklearn.utils.parse_version")
from fastapi import FastAPI
# 🔥 CORRECCIÓN PARA WINDOWS - Configurar encoding UTF-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ["PYTHONUTF8"] = "1"
    os.environ["PYTHONIOENCODING"] = "utf-8"

# Importar rutas
from app.routes import (
    analysis_routes,
    dataset_routes,
    report_routes,
    statistics_routes
)

# Importar servicios
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.utils.config import settings
from app.core import dependencies
from app.core.dataset import dataset_manager

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/sentiment_api.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Variable global para el analizador
sentiment_analyzer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestor de ciclo de vida de la aplicación"""
    global sentiment_analyzer
    
    # ========== STARTUP ==========
    logger.info("="*70)
    logger.info("SISTEMA DE ANÁLISIS DE SENTIMIENTOS UNMSM")
    logger.info("="*70)
    logger.info("Iniciando sistema...")
    
    try:
        # 1. Inicializar analizador
        logger.info("Inicializando SentimentAnalyzer...")
        sentiment_analyzer = SentimentAnalyzer()
        
        # 2. Configurar en dependencias
        dependencies.set_analyzer(sentiment_analyzer)
        logger.info("Analizador configurado en dependencias")
        
        # 3. Cargar dataset usando el dataset manager
        dataset_path = Path("data/dataset_instagram_unmsm.csv")
        if dataset_path.exists():
            try:
                logger.info(f"Cargando dataset desde: {dataset_path}")
                
                # Cargar usando el dataset manager
                dataset_loaded = dataset_manager.load_dataset(str(dataset_path))
                if dataset_loaded:
                    logger.info(f"[OK] Dataset cargado por manager: {len(dataset_manager.df)} registros")
                    
                    # Ahora cargar en el sentiment analyzer también
                    analyzer_loaded = sentiment_analyzer.load_dataset(str(dataset_path))
                    if analyzer_loaded:
                        logger.info(f"[OK] Dataset cargado en analyzer: {len(sentiment_analyzer.df)} registros")
                        
                        # Mostrar estadísticas del dataset
                        if sentiment_analyzer.df is not None and len(sentiment_analyzer.df) > 0:
                            distribution = sentiment_analyzer.df['sentimiento'].value_counts().to_dict()
                            logger.info(f"Distribución inicial: {distribution}")
                            logger.info(f"Total comentarios: {len(sentiment_analyzer.df)}")
                    else:
                        logger.error("[ERROR] Falló carga en analyzer")
                else:
                    logger.error("[ERROR] Falló carga en dataset manager")
                    
            except Exception as e:
                logger.error(f"[ERROR] Cargando dataset: {e}", exc_info=True)
                logger.info("   Sistema funcionará en modo demo")
        else:
            logger.warning(f"[WARN] Dataset no encontrado en: {dataset_path}")
            logger.info("   Sistema funcionará en modo demo")
        
        # 4. Entrenar o cargar modelo
        try:
            logger.info("Cargando/entrenando modelo ML...")
            sentiment_analyzer.load_or_train_model()
            
            if sentiment_analyzer.model:
                logger.info(" Modelo ML cargado exitosamente")
                if sentiment_analyzer.model_metadata:
                    logger.info(f" Accuracy: {sentiment_analyzer.model_metadata.get('accuracy', 0):.2%}")
            else:
                logger.warning("[WARN] Modelo no disponible")
                
        except Exception as e:
            logger.error(f"[ERROR] Con modelo ML: {e}", exc_info=True)
            logger.info("   Sistema funcionará con reglas heurísticas")
        
        logger.info("="*70)
        logger.info("[OK] SISTEMA INICIADO CORRECTAMENTE")
        logger.info(f"[API] http://{settings.HOST}:{settings.PORT}")
        logger.info(f"[DOCS] http://{settings.HOST}:{settings.PORT}/api/docs")
        logger.info("="*70)
        
    except Exception as e:
        logger.error(f"ERROR CRÍTICO en startup: {e}", exc_info=True)
        raise
    
    yield
    
    # ========== SHUTDOWN ==========
    logger.info("="*70)
    logger.info("Cerrando Sistema de Análisis de Sentimientos UNMSM...")
    logger.info("="*70)
    
    if sentiment_analyzer and sentiment_analyzer.model:
        try:
            sentiment_analyzer.save_model()
            logger.info("Modelo guardado exitosamente")
        except Exception as e:
            logger.warning(f"Error guardando modelo: {e}")
    
    logger.info("Sistema cerrado correctamente")

# Crear aplicación FastAPI
app = FastAPI(
    title="UNMSM Sentiment Analysis API",
    description="Sistema avanzado de análisis de sentimientos para la Universidad Nacional Mayor de San Marcos",
    version="3.2.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request, call_next):
    """Middleware para logging de todas las requests"""
    start_time = datetime.now()
    
    logger.info(f"[IN] {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"[OUT] {response.status_code} - {duration:.3f}s")
        return response
    except Exception as e:
        logger.error(f"[ERROR] Error procesando request: {e}")
        raise

# Incluir routers
app.include_router(
    analysis_routes.router,
    prefix="/api/analysis",
    tags=["Análisis de Sentimientos"]
)

app.include_router(
    dataset_routes.router,
    prefix="/api/dataset",
    tags=["Gestión de Dataset"]
)

app.include_router(
    report_routes.router,
    prefix="/api/reports",
    tags=["Reportes"]
)

app.include_router(
    statistics_routes.router,
    prefix="/api/statistics",
    tags=["Estadísticas"]
)

# Endpoint raíz
@app.get("/", tags=["Health Check"])
async def root():
    """Endpoint raíz con información del sistema"""
    global sentiment_analyzer
    
    dataset_info = {}
    if sentiment_analyzer and sentiment_analyzer.df is not None:
        dataset_info = {
            "total_comments": len(sentiment_analyzer.df),
            "dataset_loaded": True
        }
    else:
        dataset_info = {
            "total_comments": 0,
            "dataset_loaded": False
        }
    
    return {
        "message": "UNMSM Sentiment Analysis API v3.2",
        "status": "online",
        "university": "Universidad Nacional Mayor de San Marcos",
        "faculty": "Facultad de Ingeniería de Sistemas e Informática",
        "project": "Análisis de Sentimientos - Instagram",
        "version": "3.2.0",
        "timestamp": datetime.now().isoformat(),
        "dataset": dataset_info,
        "endpoints": {
            "docs": "/api/docs",
            "redoc": "/api/redoc",
            "health": "/health",
            "analysis": "/api/analysis",
            "dataset": "/api/dataset",
            "reports": "/api/reports",
            "statistics": "/api/statistics"
        }
    }

# Health check endpoint
@app.get("/health", tags=["Health Check"])
async def health_check():
    """Verifica el estado del sistema"""
    global sentiment_analyzer
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "online",
            "analyzer": "unknown",
            "dataset": "unknown",
            "model": "unknown"
        }
    }
    
    if sentiment_analyzer:
        health_status["components"]["analyzer"] = "online"
        
        if hasattr(sentiment_analyzer, 'df') and sentiment_analyzer.df is not None:
            health_status["components"]["dataset"] = "loaded"
            health_status["dataset_size"] = len(sentiment_analyzer.df)
            
            # Calcular distribución
            distribution = sentiment_analyzer.df['sentimiento'].value_counts().to_dict()
            health_status["dataset_distribution"] = distribution
        else:
            health_status["components"]["dataset"] = "not_loaded"
        
        if hasattr(sentiment_analyzer, 'model') and sentiment_analyzer.model is not None:
            health_status["components"]["model"] = "loaded"
            if sentiment_analyzer.model_metadata:
                health_status["model_accuracy"] = f"{sentiment_analyzer.model_metadata.get('accuracy', 0):.2%}"
        else:
            health_status["components"]["model"] = "not_loaded"
    else:
        health_status["status"] = "degraded"
        health_status["components"]["analyzer"] = "offline"
    
    return health_status

# Nuevo endpoint para verificar dataset
@app.get("/dataset/info", tags=["Dataset"])
async def dataset_info():
    """Información detallada del dataset cargado"""
    global sentiment_analyzer
    
    if not sentiment_analyzer or sentiment_analyzer.df is None:
        raise HTTPException(status_code=404, detail="Dataset no cargado")
    
    try:
        df = sentiment_analyzer.df
        
        # Calcular estadísticas
        total_comments = len(df)
        distribution = df['sentimiento'].value_counts().to_dict()
        
        # Calcular porcentajes
        percentages = {}
        for sentiment, count in distribution.items():
            percentages[sentiment] = round((count / total_comments) * 100, 2)
        
        # Obtener muestra de comentarios
        sample_comments = []
        for sentiment in ['Positivo', 'Neutral', 'Negativo']:
            if sentiment in df['sentimiento'].values:
                sample = df[df['sentimiento'] == sentiment]['comentario'].head(3).tolist()
                sample_comments.append({
                    "sentiment": sentiment,
                    "comments": sample
                })
        
        return {
            "total_comments": total_comments,
            "distribution": distribution,
            "percentages": percentages,
            "sample_comments": sample_comments,
            "columns": list(df.columns),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo info del dataset: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Handler de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejador global de excepciones"""
    logger.error(f"[ERROR] Error no manejado: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Ha ocurrido un error interno en el servidor",
            "detail": str(exc) if settings.DEBUG else "Contacta al administrador",
            "timestamp": datetime.now().isoformat()
        }
    )

# Handler para 404
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Manejador de rutas no encontradas"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"La ruta {request.url.path} no existe",
            "available_routes": [
                "/api/docs",
                "/health",
                "/dataset/info",
                "/api/analysis/single",
                "/api/analysis/batch",
                "/api/dataset/info",
                "/api/reports/generate",
                "/api/statistics"
            ],
            "timestamp": datetime.now().isoformat()
        }
    )

# Ejecutar servidor
if __name__ == "__main__":
    print("="*70)
    print("SISTEMA DE ANÁLISIS DE SENTIMIENTOS - UNMSM")
    print("="*70)
    print(f"Servidor: http://{settings.HOST}:{settings.PORT}")
    print(f"Documentación: http://{settings.HOST}:{settings.PORT}/api/docs")
    print(f"ReDoc: http://{settings.HOST}:{settings.PORT}/api/redoc")
    print("="*70)
    print("\nIniciando servidor FastAPI...\n")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True
    )
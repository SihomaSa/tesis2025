"""
RUTAS DE GESTIÓN DE DATASET - API UNMSM
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
import logging
import pandas as pd
from pathlib import Path

from app.schemas import DatasetInfo, ModelTrainingResponse, ErrorResponse
from app.core.dependencies import get_sentiment_analyzer
from app.utils.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/info",
    response_model=DatasetInfo,
    summary="Información del dataset",
    description="Obtiene información del dataset cargado"
)
async def get_dataset_info(analyzer=Depends(get_sentiment_analyzer)):
    """Obtiene información sobre el dataset actual"""
    try:
        if analyzer.df is None:
            raise HTTPException(
                status_code=404,
                detail="No hay dataset cargado"
            )
        
        info = DatasetInfo(
            total_records=len(analyzer.df),
            columns=analyzer.df.columns.tolist(),
            sentiment_distribution=analyzer.df['Rating'].value_counts().to_dict(),
            date_loaded=analyzer.df.attrs.get('load_date', None)
        )
        
        logger.info(f"✅ Info del dataset obtenida: {info.total_records} registros")
        
        return info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error obteniendo info del dataset: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )


@router.post(
    "/upload",
    summary="Cargar dataset",
    description="Carga un nuevo dataset CSV"
)
async def upload_dataset(
    file: UploadFile = File(...),
    analyzer=Depends(get_sentiment_analyzer)
):
    """Carga un archivo CSV como dataset"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400,
                detail="El archivo debe ser formato CSV"
            )
        
        # Guardar archivo
        file_path = settings.DATA_DIR / file.filename
        
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # Cargar dataset
        analyzer.load_dataset(str(file_path))
        
        logger.info(f"✅ Dataset cargado desde: {file.filename}")
        
        return {
            "message": "Dataset cargado exitosamente",
            "filename": file.filename,
            "records": len(analyzer.df),
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error cargando dataset: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error cargando archivo: {str(e)}"
        )


@router.post(
    "/train-model",
    response_model=ModelTrainingResponse,
    summary="Entrenar modelo",
    description="Entrena un nuevo modelo ML con el dataset actual"
)
async def train_model(analyzer=Depends(get_sentiment_analyzer)):
    """Entrena un nuevo modelo con el dataset cargado"""
    try:
        if analyzer.df is None:
            raise HTTPException(
                status_code=404,
                detail="No hay dataset cargado. Carga un dataset primero."
            )
        
        logger.info("🤖 Iniciando entrenamiento del modelo...")
        
        # Entrenar
        metadata = analyzer.train_model()
        
        # Guardar modelo
        analyzer.save_model()
        
        response = ModelTrainingResponse(
            status="completed",
            accuracy=metadata['accuracy'],
            f1_weighted=metadata['f1_weighted'],
            train_size=metadata['train_size'],
            test_size=metadata['test_size'],
            features=metadata['features'],
            training_date=metadata['training_date']
        )
        
        logger.info(f"✅ Modelo entrenado exitosamente - Accuracy: {response.accuracy:.2%}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error entrenando modelo: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en entrenamiento: {str(e)}"
        )
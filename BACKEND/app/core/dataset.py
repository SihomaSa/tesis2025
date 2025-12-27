"""
Módulo de gestión de dataset - UNMSM Sentiment Analysis
Proporciona acceso al dataset de comentarios de Instagram
"""

import pandas as pd
from pathlib import Path
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class DatasetManager:
    """Gestor del dataset de comentarios"""
    
    def __init__(self):
        self.df = None
        self.dataset_path = None
        self.is_loaded_flag = False
    
    def load_dataset(self, filepath: str) -> bool:
        """
        Carga el dataset desde un archivo CSV
        
        Args:
            filepath: Ruta al archivo CSV
            
        Returns:
            bool: True si se cargó exitosamente
        """
        try:
            path = Path(filepath)
            if not path.exists():
                logger.warning(f"Dataset no encontrado en: {filepath}")
                return False
            
            self.df = pd.read_csv(filepath)
            self.dataset_path = filepath
            self.is_loaded_flag = True
            
            logger.info(f"Dataset cargado: {len(self.df)} registros")
            
            # Verificar columnas necesarias
            required_columns = ['comentario', 'sentimiento']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                logger.warning(f"Columnas faltantes: {missing_columns}")
                # Crear columnas faltantes si es necesario
                for col in missing_columns:
                    if col == 'sentimiento':
                        self.df[col] = 'Neutral'  # Valor por defecto
                    else:
                        self.df[col] = ''
            
            return True
            
        except Exception as e:
            logger.error(f"Error cargando dataset: {e}")
            return False
    
    def is_loaded(self) -> bool:
        """Verifica si el dataset está cargado"""
        return self.is_loaded_flag and self.df is not None
    
    def get_dataframe(self) -> pd.DataFrame:
        """Obtiene el DataFrame del dataset"""
        if not self.is_loaded():
            raise ValueError("Dataset no cargado")
        return self.df
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas básicas del dataset"""
        if not self.is_loaded():
            return {"error": "Dataset no cargado"}
        
        try:
            stats = {
                "total_comments": len(self.df),
                "distribution": self.df['sentimiento'].value_counts().to_dict(),
                "columns": list(self.df.columns),
                "sample_comments": self.df['comentario'].head(5).tolist() if 'comentario' in self.df.columns else []
            }
            
            # Calcular longitud promedio de comentarios
            if 'comentario' in self.df.columns:
                avg_length = self.df['comentario'].astype(str).apply(len).mean()
                stats["avg_comment_length"] = float(avg_length)
            else:
                stats["avg_comment_length"] = 0
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculando estadísticas: {e}")
            return {"error": str(e)}
    
    def get_comments_by_sentiment(self, sentiment: str, limit: int = 10) -> List[str]:
        """Obtiene comentarios por sentimiento"""
        if not self.is_loaded() or 'sentimiento' not in self.df.columns:
            return []
        
        filtered = self.df[self.df['sentimiento'] == sentiment]
        if 'comentario' in filtered.columns:
            return filtered['comentario'].head(limit).tolist()
        return []
    
    def add_comment(self, comment: str, sentiment: str) -> bool:
        """Agrega un nuevo comentario al dataset"""
        if not self.is_loaded():
            return False
        
        try:
            new_row = pd.DataFrame([{
                'comentario': comment,
                'sentimiento': sentiment
            }])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            return True
        except Exception as e:
            logger.error(f"Error agregando comentario: {e}")
            return False

# Instancia global del gestor de dataset
dataset_manager = DatasetManager()
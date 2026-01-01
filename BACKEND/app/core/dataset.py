import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DatasetManager:
    """Gestor de dataset simplificado"""
    
    def __init__(self):
        self.df = None
    
    def load_dataset(self, filepath: str) -> pd.DataFrame:
        """
        Carga el dataset desde un archivo CSV
        """
        try:
            logger.info(f"Cargando dataset desde: {filepath}")
            self.df = pd.read_csv(filepath, encoding="utf-8")
            logger.info(f"Dataset cargado: {len(self.df)} registros")
            
            # Normalizar columnas
            self.df.columns = [col.strip().lower() for col in self.df.columns]
            
            # Mapeo automático
            for col in self.df.columns:
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in ['texto', 'comentario', 'comment']):
                    self.df = self.df.rename(columns={col: 'comentario'})
                    print(f"📝 Columna renombrada: {col} -> comentario")
                    break
            
            for col in self.df.columns:
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in ['sentimiento', 'sentiment', 'rating']):
                    self.df = self.df.rename(columns={col: 'sentimiento'})
                    print(f"📝 Columna renombrada: {col} -> sentimiento")
                    break
            
            # Verificar que tenemos las columnas necesarias
            if 'comentario' not in self.df.columns:
                print("⚠️  No se encontró columna 'comentario', usando primera columna")
                self.df = self.df.rename(columns={self.df.columns[0]: 'comentario'})
            
            if 'sentimiento' not in self.df.columns:
                print("⚠️  No se encontró columna 'sentimiento', creando columna neutral")
                self.df['sentimiento'] = 'Neutral'
            
            print(f"✅ Columnas finales: {list(self.df.columns)}")
            return self.df
            
        except Exception as e:
            logger.error(f"Error cargando dataset: {e}")
            print(f"❌ Error: {e}")
            raise

# Instancia global para importación
dataset_manager = DatasetManager()

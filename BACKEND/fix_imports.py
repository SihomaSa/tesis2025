import os

print("=== CORRIGIENDO ERRORES DE IMPORTACIÓN ===")

# 1. Corregir dataset.py
dataset_path = 'app/core/dataset.py'
print(f"Corrigiendo {dataset_path}...")

dataset_content = '''import pandas as pd
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
'''

# Guardar dataset.py
os.makedirs('app/core', exist_ok=True)
with open(dataset_path, 'w', encoding='utf-8') as f:
    f.write(dataset_content)

print("✅ dataset.py corregido")

# 2. Corregir __init__.py en app/core
init_path = 'app/core/__init__.py'
print(f"\nCorrigiendo {init_path}...")

init_content = '''"""
Módulo core de la aplicación
"""

from .dataset import dataset_manager, DatasetManager

__all__ = ['dataset_manager', 'DatasetManager']
'''

with open(init_path, 'w', encoding='utf-8') as f:
    f.write(init_content)

print("✅ __init__.py corregido")

# 3. Verificar estructura de imports en dependencies.py
print("\n📋 Verificando app/core/dependencies.py...")

# Crear dependencies.py si no existe
dependencies_path = 'app/core/dependencies.py'
if not os.path.exists(dependencies_path):
    print(f"Creando {dependencies_path}...")
    
    dependencies_content = '''"""
Dependencias del sistema
"""
import logging
from app.services.sentiment_analyzer import SentimentAnalyzer

logger = logging.getLogger(__name__)

# Instancia global del analizador de sentimientos
_sentiment_analyzer = None

def get_sentiment_analyzer() -> SentimentAnalyzer:
    """
    Retorna la instancia del analizador de sentimientos
    (patrón singleton)
    """
    global _sentiment_analyzer
    
    if _sentiment_analyzer is None:
        logger.info("Creando nueva instancia de SentimentAnalyzer")
        _sentiment_analyzer = SentimentAnalyzer()
        
        # Intentar cargar dataset por defecto
        try:
            dataset_path = "data/dataset_instagram_unmsm.csv"
            _sentiment_analyzer.load_dataset(dataset_path)
            logger.info("✅ Dataset cargado automáticamente")
        except Exception as e:
            logger.warning(f"No se pudo cargar dataset automáticamente: {e}")
    
    return _sentiment_analyzer
'''
    
    os.makedirs('app/core', exist_ok=True)
    with open(dependencies_path, 'w', encoding='utf-8') as f:
        f.write(dependencies_content)
    
    print("✅ dependencies.py creado")
else:
    print(f"✅ {dependencies_path} ya existe")

print("\n🎯 CORRECCIONES APLICADAS:")
print("1. dataset.py ahora exporta dataset_manager")
print("2. __init__.py importa correctamente")
print("3. Dependencias verificadas")

print("\n📁 Estructura actual de app/core/:")
for root, dirs, files in os.walk('app/core'):
    level = root.replace('app/core', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        print(f'{subindent}{file}')
"""
SCRIPT DE EJECUCIÓN - BACKEND UNMSM
Ejecuta el servidor de desarrollo
"""

import uvicorn
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from app.utils.config import settings

if __name__ == "__main__":
    print("="*70)
    print("🎓 SISTEMA DE ANÁLISIS DE SENTIMIENTOS - UNMSM")
    print("="*70)
    print(f"🌐 Servidor: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 Documentación: http://{settings.HOST}:{settings.PORT}/api/docs")
    print(f"📖 ReDoc: http://{settings.HOST}:{settings.PORT}/api/redoc")
    print("="*70)
    print("\n🚀 Iniciando servidor FastAPI...\n")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True
    )
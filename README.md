# 🎓 UNMSM Sentiment Analysis API

Sistema avanzado de análisis de sentimientos para comentarios de Instagram de la Universidad Nacional Mayor de San Marcos.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-orange)](https://scikit-learn.org)
[![Railway](https://img.shields.io/badge/Railway-Deploy-purple)](https://railway.app)

## 📋 Características

- ✅ Análisis de sentimientos en tiempo real (Positivo/Neutral/Negativo)
- ✅ Modelo ML entrenado con 868 comentarios reales
- ✅ API REST completa con FastAPI
- ✅ Análisis por lotes
- ✅ Estadísticas detalladas
- ✅ Análisis por temas/categorías
- ✅ Palabras más comunes
- ✅ Generación de reportes
- ✅ Dashboard interactivo

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.12+
- pip
- Git

### Instalación Local

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/unmsm-sentiment-api.git
cd unmsm-sentiment-api

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar dataset
ls -lh data/dataset_instagram_unmsm.csv

# 5. Ejecutar servidor
python run.py
```

El servidor estará disponible en:
- API: http://localhost:8000/api
- Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 📡 Endpoints Principales

### Health Check
```bash
GET /health
```

### Análisis de Sentimientos

#### Comentario Individual
```bash
POST /api/analysis/single
Content-Type: application/json

{
  "text": "La UNMSM tiene excelentes profesores",
  "include_details": true
}
```

#### Análisis por Lotes
```bash
POST /api/analysis/batch
Content-Type: application/json

{
  "texts": [
    "Excelente universidad",
    "Pésimo servicio",
    "Ambiente regular"
  ]
}
```

### Estadísticas

#### Estadísticas Generales
```bash
GET /api/statistics/
```

#### Análisis por Temas
```bash
GET /api/statistics/topics
```

#### Datos del Dashboard
```bash
GET /api/statistics/dashboard-data
```

### Reportes
```bash
POST /api/reports/generate
Content-Type: application/json

{
  "period": "current",
  "format": "json"
}
```

## 📊 Dataset

El sistema utiliza un dataset de 868 comentarios de Instagram con las siguientes columnas:

- `comentario`: Texto del comentario
- `sentimiento`: Clasificación (Positivo/Neutral/Negativo)

**Ubicación:** `data/dataset_instagram_unmsm.csv`

## 🤖 Modelo ML

- **Algoritmo:** Logistic Regression + TF-IDF
- **Accuracy:** ~82%
- **Features:** 
  - Score de emojis
  - Palabras positivas/negativas
  - Longitud del comentario
  - Diferencia de sentimientos

## 🏗️ Estructura del Proyecto

```
BACKEND/
├── app/
│   ├── main.py              # Aplicación principal
│   ├── routes/              # Endpoints
│   │   ├── analysis_routes.py
│   │   ├── statistics_routes.py
│   │   ├── dataset_routes.py
│   │   └── report_routes.py
│   ├── services/            # Lógica de negocio
│   │   └── sentiment_analyzer.py
│   ├── schemas/             # Modelos Pydantic
│   │   ├── schemas.py
│   │   └── analysis.py
│   ├── core/                # Configuración
│   │   ├── dependencies.py
│   │   └── dataset.py
│   └── utils/               # Utilidades
│       └── config.py
├── data/
│   └── dataset_instagram_unmsm.csv  # Dataset
├── ml_models/               # Modelos entrenados
├── requirements.txt         # Dependencias
├── railway.json             # Config Railway
├── nixpacks.toml           # Config Nixpacks
├── Procfile                # Process file
├── build.sh                # Script de build
├── start.sh                # Script de inicio
├── verify-deployment.sh    # Verificación
└── run.py                  # Ejecutar servidor
```

## 🚢 Despliegue en Railway

### Preparación

```bash
# 1. Verificar todo está listo
chmod +x verify-deployment.sh
./verify-deployment.sh

# 2. Hacer scripts ejecutables
chmod +x build.sh start.sh

# 3. Commit cambios
git add .
git commit -m "Ready for deployment"
git push
```

### Desplegar

#### Opción 1: Desde GitHub (Recomendado)

1. Push a GitHub
2. Conectar con Railway
3. Railway detecta automáticamente la configuración
4. ¡Listo!

#### Opción 2: Railway CLI

```bash
# Instalar CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar
railway init

# Desplegar
railway up
```

### Variables de Entorno (Railway)

```
PORT=8000
HOST=0.0.0.0
PYTHONUNBUFFERED=1
DEBUG=False
```

### Verificar Despliegue

```bash
# Health check
curl https://tu-app.railway.app/health

# Estadísticas
curl https://tu-app.railway.app/api/statistics/

# Análisis
curl -X POST https://tu-app.railway.app/api/analysis/single \
  -H "Content-Type: application/json" \
  -d '{"text": "Excelente universidad", "include_details": true}'
```

## 🔧 Configuración Frontend Angular

```typescript
// src/environments/environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://tu-app.railway.app/api'
};
```

## 📚 Documentación API

Una vez desplegado, accede a:

- **Swagger UI:** `https://tu-app.railway.app/api/docs`
- **ReDoc:** `https://tu-app.railway.app/api/redoc`
- **OpenAPI JSON:** `https://tu-app.railway.app/openapi.json`

## 🧪 Testing

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app tests/
```

## 📈 Monitoreo

```bash
# Ver logs
railway logs

# Ver logs en tiempo real
railway logs --tail

# Estado del servicio
railway status

# Variables
railway variables
```

## 🐛 Solución de Problemas

### Dataset no encontrado
```bash
# Verificar que el dataset existe
ls -lh data/dataset_instagram_unmsm.csv

# Añadir al repositorio si no está
git add data/dataset_instagram_unmsm.csv -f
git commit -m "Add dataset"
git push
```

### Error de módulos
```bash
# Actualizar requirements
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Error de permisos
```bash
chmod +x build.sh start.sh
git add build.sh start.sh
git commit -m "Fix permissions"
git push
```

### CORS issues
Verifica en `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

## 👥 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Contacto

UNMSM - Facultad de Ingeniería de Sistemas

---

⭐ Si este proyecto te fue útil, dale una estrella en GitHub!

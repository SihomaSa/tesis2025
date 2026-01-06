# 🎓 Análisis de Sentimientos - UNMSM

Sistema de análisis de sentimientos para evaluar la percepción de la comunidad universitaria de la Universidad Nacional Mayor de San Marcos en redes sociales (Instagram).

![Universidad Nacional Mayor de San Marcos](https://img.shields.io/badge/Universidad-UNMSM-red?style=for-the-badge)
![Angular](https://img.shields.io/badge/Angular-18-DD0031?style=for-the-badge&logo=angular)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)
![Firebase](https://img.shields.io/badge/Firebase-Hosting-FFCA28?style=for-the-badge&logo=firebase)

## 🌐 Demo en Vivo

- **Frontend:** [https://analysis-sentiment-unmsm.web.app](https://analysis-sentiment-unmsm.web.app)
- **Backend API:** https://tesis2025-production.up.railway.app
- **Documentación API:** https://tesis2025-production.up.railway.app]/api/docs

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso](#-uso)
- [API Documentation](#-api-documentation)
- [Despliegue](#-despliegue)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Autores](#-autores)

## ✨ Características

### Frontend (Angular 18)
- 🎨 **Dashboard Interactivo** con visualizaciones en tiempo real
- 📊 **Gráficos Dinámicos** usando SVG nativo y librerías especializadas
- 📄 **Exportación a PDF** de reportes ejecutivos con alta calidad
- 🔐 **Autenticación** con Firebase Authentication
- 📱 **Diseño Responsive** adaptado a todos los dispositivos
- 🌓 **Modo Oscuro/Claro** (próximamente)
- 🔄 **Actualización en Tiempo Real** de estadísticas

### Backend (Python + FastAPI)
- 🤖 **Análisis de Sentimientos** usando Machine Learning (RandomForest)
- 📈 **Procesamiento de Lenguaje Natural (NLP)** con NLTK y spaCy
- 🗂️ **API RESTful** documentada con OpenAPI/Swagger
- 💾 **Caché Inteligente** para optimización de rendimiento
- 📊 **Generación de Reportes** ejecutivos y estadísticos
- 🔍 **Análisis de Temas** y palabras más frecuentes
- ⚡ **Procesamiento Asíncrono** para grandes volúmenes de datos

### Análisis de Datos
- 📊 **Dataset:** 3,312+ comentarios de Instagram
- 🎯 **Clasificación:** Positivo, Neutral, Negativo
- 📈 **Métricas:** Precisión del 86%+
- 🏷️ **Categorías:** Enseñanza, Infraestructura, Servicios, Tecnología
- 📅 **Análisis Temporal:** Tendencias por mes/trimestre/año

## 🏗️ Arquitectura

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│                 │         │                  │         │             │
│  Angular 18     │◄───────►│  FastAPI Backend │◄───────►│  Firebase   │
│  Frontend       │  HTTPS  │  Python 3.11     │  Auth   │  Services   │
│                 │         │                  │         │             │
└─────────────────┘         └──────────────────┘         └─────────────┘
        │                           │
        │                           │
        ▼                           ▼
┌─────────────────┐         ┌──────────────────┐
│                 │         │                  │
│  Firebase       │         │  ML Models       │
│  Hosting        │         │  Dataset (CSV)   │
│                 │         │                  │
└─────────────────┘         └──────────────────┘
```

## 🛠️ Tecnologías

### Frontend
- **Framework:** Angular 18.2.0 (Standalone Components)
- **Lenguaje:** TypeScript 5.5
- **Estilos:** SCSS + CSS Custom Properties
- **Gráficos:** SVG Nativo
- **Autenticación:** Firebase Auth
- **Hosting:** Firebase Hosting
- **Exportación PDF:** html2pdf.js
- **HTTP Client:** Angular HttpClient
- **Routing:** Angular Router

### Backend
- **Framework:** FastAPI 0.104+
- **Lenguaje:** Python 3.11
- **ML/NLP:**
  - scikit-learn (RandomForest, TfidfVectorizer)
  - NLTK (tokenización, stopwords)
  - spaCy (procesamiento avanzado)
  - pandas, numpy (manipulación de datos)
- **API Docs:** Swagger/OpenAPI
- **CORS:** FastAPI CORS Middleware
- **Servidor:** Uvicorn (ASGI)
- **Deployment:** Railway / Docker

### DevOps
- **Containerización:** Docker + Docker Compose
- **CI/CD:** GitHub Actions (próximamente)
- **Hosting Backend:** Railway
- **Hosting Frontend:** Firebase
- **Version Control:** Git + GitHub

## 📦 Requisitos Previos

### Para el Frontend
- Node.js 20+ y npm 10+
- Angular CLI 18+
- Firebase CLI

### Para el Backend
- Python 3.11+
- pip (package manager)
- Docker (opcional, para containerización)

### Opcional
- Git
- Visual Studio Code o tu IDE preferido

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/analysis-sentiment-unmsm.git
cd analysis-sentiment-unmsm
```

### 2. Configurar el Backend

```bash
cd BACKEND

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar recursos de NLTK (primera vez)
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Configurar variables de entorno (crear .env)
cat > .env << EOF
ENVIRONMENT=development
PORT=8000
ALLOWED_ORIGINS=http://localhost:4200
EOF

# Iniciar servidor de desarrollo
python main.py
```

El backend estará disponible en: `http://localhost:8000`

### 3. Configurar el Frontend

```bash
cd ../analysis-sentiment-unmsm

# Instalar dependencias
npm install

# Configurar Firebase (si es necesario)
# Edita src/environments/environment.ts con tus credenciales

# Iniciar servidor de desarrollo
npm start
```

El frontend estará disponible en: `http://localhost:4200`

## 💻 Uso

### Desarrollo Local

```bash
# Terminal 1 - Backend
cd BACKEND
python main.py

# Terminal 2 - Frontend
cd analysis-sentiment-unmsm
npm start
```

Abre tu navegador en `http://localhost:4200`

### Funcionalidades Principales

1. **Dashboard Principal**
   - Visualiza métricas generales de sentimientos
   - Gráficos de distribución y tendencias
   - Estadísticas en tiempo real

2. **Análisis Detallado**
   - Filtra por fechas, categorías
   - Exporta reportes a PDF
   - Visualiza comentarios individuales

3. **Reportes Ejecutivos**
   - Genera reportes académicos
   - Análisis por categorías
   - Recomendaciones automáticas

## 📚 API Documentation

### Endpoints Principales

#### Health Check
```http
GET /health
```
Verifica el estado del servidor.

#### Dashboard Data
```http
GET /api/statistics/dashboard-data
```
Obtiene todas las métricas del dashboard.

**Respuesta:**
```json
{
  "metrics": {
    "total_comments": 3312,
    "sentiment_distribution": {
      "Positivo": 2246,
      "Neutral": 549,
      "Negativo": 517
    },
    "sentiment_percentages": {
      "Positivo": 67.8,
      "Neutral": 16.6,
      "Negativo": 15.6
    }
  },
  "model_info": {
    "accuracy": 0.86,
    "model_type": "RandomForest"
  }
}
```

#### Análisis de Sentimientos
```http
POST /api/analysis/predict
Content-Type: application/json

{
  "text": "Excelente universidad, los profesores son muy buenos"
}
```

**Respuesta:**
```json
{
  "sentiment": "Positivo",
  "confidence": 0.92,
  "probabilities": {
    "Positivo": 0.92,
    "Neutral": 0.05,
    "Negativo": 0.03
  }
}
```

### Documentación Completa

Accede a la documentación interactiva en:
- **Swagger UI:** `http://localhost:8000/api/docs`
- **ReDoc:** `http://localhost:8000/api/redoc`

## 🚀 Despliegue

### Backend en Railway

1. **Conectar Repositorio**
   ```bash
   # Asegúrate de tener el código en GitHub
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Configurar Railway**
   - Ve a [railway.app](https://railway.app)
   - Conecta tu repositorio de GitHub
   - Selecciona `BACKEND` como directorio raíz
   - Configura variables de entorno:
     ```
     PORT=8000
     ENVIRONMENT=production
     ALLOWED_ORIGINS=https://analysis-sentiment-unmsm.web.app
     ```
   - Deploy automático

3. **Obtener URL**
   - Railway te dará una URL como: `https://tu-proyecto.railway.app`

### Frontend en Firebase

1. **Instalar Firebase CLI**
   ```bash
   npm install -g firebase-tools
   ```

2. **Login y configurar**
   ```bash
   firebase login
   firebase init hosting
   ```

3. **Actualizar URL del Backend**
   ```typescript
   // src/environments/environment.prod.ts
   export const environment = {
     production: true,
     backendUrl: 'https://tu-proyecto.railway.app/api',
     apiUrl: 'https://tu-proyecto.railway.app/api',
     mlApiUrl: 'https://tu-proyecto.railway.app',
     // ...
   };
   ```

4. **Build y Deploy**
   ```bash
   npm run build -- --configuration production
   firebase deploy
   ```

### Usando Docker Compose (Opcional)

```bash
# Build y ejecutar todo el stack
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

## 📁 Estructura del Proyecto

```
analysis-sentiment-unmsm/
├── BACKEND/                          # Backend FastAPI
│   ├── app/
│   │   ├── routes/                   # Endpoints de la API
│   │   ├── services/                 # Lógica de negocio
│   │   ├── models/                   # Modelos de datos
│   │   └── utils/                    # Utilidades
│   ├── ml_models/                    # Modelos de Machine Learning
│   ├── data/                         # Datasets
│   ├── main.py                       # Punto de entrada
│   ├── requirements.txt              # Dependencias Python
│   └── Dockerfile                    # Docker configuration
│
├── analysis-sentiment-unmsm/         # Frontend Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/                 # Servicios core
│   │   │   ├── features/             # Módulos de funcionalidades
│   │   │   ├── shared/               # Componentes compartidos
│   │   │   └── models/               # Interfaces TypeScript
│   │   ├── environments/             # Configuraciones de entorno
│   │   └── assets/                   # Recursos estáticos
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
│
├── Datasets/                         # Datos de entrenamiento
├── docker-compose.yml                # Orquestación de servicios
├── .gitignore
└── README.md                         # Este archivo
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código

- **Frontend:** Sigue las guías de estilo de Angular
- **Backend:** Sigue PEP 8 para Python
- **Commits:** Usa Conventional Commits

## 📄 Licencia

Este proyecto es parte de una tesis de grado de la Universidad Nacional Mayor de San Marcos.

## 👥 Autores

**Facultad de Ingeniería de Sistemas e Informática**
Universidad Nacional Mayor de San Marcos

- **Desarrollador Principal:** [Tu Nombre]
- **Asesor:** [Nombre del Asesor]
- **Año:** 2025

## 🙏 Agradecimientos

- Universidad Nacional Mayor de San Marcos
- Facultad de Ingeniería de Sistemas e Informática
- Comunidad de código abierto

## 📞 Contacto

- **Email:** sihomara.ochoa@unmsm.edu.pe
- **Universidad:** [UNMSM](https://www.unmsm.edu.pe)
- **LinkedIn:** https://www.linkedin.com/in/sihomara-sandy-ochoa-cisneros/

---

<div align="center">

**🎓 Hecho con ❤️ en la UNMSM - La universidad del Perú, Decana de América**

[![UNMSM](https://img.shields.io/badge/UNMSM-1551-red?style=for-the-badge)](https://www.unmsm.edu.pe)

</div>

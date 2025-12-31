// server.js
const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS ? process.env.ALLOWED_ORIGINS.split(',') : '*',
  credentials: true
}));

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Servir archivos estáticos si existe build
app.use(express.static(path.join(__dirname, 'public')));

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'UNMSM Sentiment Analysis API',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development'
  });
});

// Info endpoint
app.get('/api/info', (req, res) => {
  res.json({
    name: 'UNMSM Sentiment Analysis API',
    version: '3.2.0',
    description: 'Sistema de análisis de sentimientos para la Universidad Nacional Mayor de San Marcos',
    endpoints: {
      health: '/api/health',
      docs: '/api/docs',
      analysis: '/api/analysis',
      dataset: '/api/dataset'
    }
  });
});

// Ruta principal
app.get('/', (req, res) => {
  res.json({
    message: 'Bienvenido a la API de Análisis de Sentimientos UNMSM',
    documentation: '/api/docs',
    health_check: '/api/health'
  });
});

// Para Railway: usar el puerto que asigne Railway
const PORT = process.env.PORT || 8080;

app.listen(PORT, () => {
  console.log(`🚀 Servidor ejecutándose en puerto ${PORT}`);
  console.log(`📚 Documentación disponible en http://localhost:${PORT}/api/docs`);
  console.log(`🏥 Health check: http://localhost:${PORT}/api/health`);
});
# Usar imagen oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY BACKEND/requirements.txt .

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el contenido de BACKEND
COPY BACKEND/ .

# Crear directorios necesarios
RUN mkdir -p logs data

# DEBUG: Ver estructura de archivos
RUN echo "=== Contenido de /app ===" && ls -la /app && \
    echo "=== Contenido de /app/app ===" && ls -la /app/app 2>/dev/null || echo "No hay carpeta app"

# Exponer el puerto
EXPOSE 8000

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Iniciar la aplicación
# Si main.py está en /app/main.py, usa esto:
CMD ["python", "main.py"]

# Si quieres usar uvicorn directamente (alternativa):
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
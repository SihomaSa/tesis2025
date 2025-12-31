# Usar imagen oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el contenido del BACKEND al contenedor
COPY . .

# Crear directorios necesarios
RUN mkdir -p logs data

# DEBUG: Ver estructura de archivos
RUN echo "=== Contenido de /app ===" && ls -la /app && \
    echo "=== Contenido de /app/app ===" && ls -la /app/app && \
    echo "=== Archivos .py en /app/app ===" && find /app/app -name "*.py" | head -10

# Exponer el puerto
EXPOSE 8000

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# OPCIÓN 1: Cambiar el CMD para apuntar a app/main.py
CMD ["python", "app/main.py"]

# OPCIÓN 2: Usar uvicorn con el módulo correcto
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
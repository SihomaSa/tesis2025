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
COPY BACKEND/ /app/

# Crear directorio de logs
RUN mkdir -p /app/logs

# Exponer el puerto
EXPOSE 8000

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Comando para iniciar - usando uvicorn directamente
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
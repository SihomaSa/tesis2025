#!/bin/bash

echo "🚀 Desplegando UNMSM Sentiment Analysis..."

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -d "inspiring_pike" ]; then
    echo -e "${RED}❌ Error: No se encuentra la carpeta 'inspiring_pike'${NC}"
    echo "Asegúrate de estar en el directorio raíz del proyecto"
    exit 1
fi

# 1. Detener contenedores existentes
echo -e "${BLUE}📦 Deteniendo contenedores existentes...${NC}"
docker-compose down 2>/dev/null || true

# 2. Limpiar imágenes antiguas (opcional)
echo -e "${BLUE}🧹 Limpiando imágenes antiguas...${NC}"
docker image prune -f

# 3. Build SOLO del backend
echo -e "${BLUE}🔨 Construyendo backend...${NC}"
docker-compose build backend

# 4. Iniciar SOLO el backend
echo -e "${BLUE}🚀 Iniciando backend...${NC}"
docker-compose up -d backend

# 5. Esperar a que el backend esté listo
echo -e "${BLUE}⏳ Esperando a que el backend esté listo...${NC}"
sleep 10

# 6. Verificar estado
echo -e "${BLUE}✅ Verificando estado...${NC}"
docker-compose ps

# 7. Verificar salud del backend
echo -e "${BLUE}🏥 Verificando salud del backend...${NC}"
curl -s http://localhost:8000/health | jq '.' || echo -e "${RED}Backend no responde${NC}"

# 8. Mostrar logs
echo -e "${GREEN}📋 Últimos logs del backend:${NC}"
docker-compose logs backend --tail=30

echo ""
echo -e "${GREEN}✅ ¡Despliegue completado!${NC}"
echo -e "${GREEN}📍 Backend API: http://localhost:8000${NC}"
echo -e "${GREEN}📍 API Docs: http://localhost:8000/api/docs${NC}"
echo -e "${GREEN}📍 Health Check: http://localhost:8000/health${NC}"
echo ""
echo -e "${BLUE}💡 Comandos útiles:${NC}"
echo "  Ver logs:      docker-compose logs -f backend"
echo "  Reiniciar:     docker-compose restart backend"
echo "  Detener:       docker-compose down"
echo ""

# Monitoreo continuo (opcional)
echo -e "${BLUE}👀 ¿Ver logs en tiempo real? (y/n)${NC}"
read -r response
if [[ "$response" == "y" ]]; then
    docker-compose logs -f backend
fi
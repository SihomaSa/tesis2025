#!/bin/bash

echo "=================================================="
echo "🔍 VERIFICACIÓN PRE-DESPLIEGUE - UNMSM SENTIMENT"
echo "=================================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Función para verificar
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
        ((ERRORS++))
    fi
}

check_warning() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${YELLOW}⚠${NC} $1"
        ((WARNINGS++))
    fi
}

echo "1. VERIFICANDO ESTRUCTURA DE ARCHIVOS"
echo "--------------------------------------"

# Archivos críticos
test -f "app/main.py"
check "app/main.py existe"

test -f "requirements.txt"
check "requirements.txt existe"

test -f "data/dataset_instagram_unmsm.csv"
check "Dataset existe (CRÍTICO)"

test -f "railway.json"
check_warning "railway.json existe"

test -f "nixpacks.toml"
check_warning "nixpacks.toml existe"

test -f "Procfile"
check_warning "Procfile existe"

echo ""
echo "2. VERIFICANDO SCRIPTS"
echo "----------------------"

test -f "build.sh"
check "build.sh existe"

test -x "build.sh"
check_warning "build.sh es ejecutable"

test -f "start.sh"
check "start.sh existe"

test -x "start.sh"
check_warning "start.sh es ejecutable"

echo ""
echo "3. VERIFICANDO DATASET"
echo "----------------------"

if [ -f "data/dataset_instagram_unmsm.csv" ]; then
    LINES=$(wc -l < data/dataset_instagram_unmsm.csv)
    if [ $LINES -gt 1 ]; then
        echo -e "${GREEN}✓${NC} Dataset tiene $LINES líneas"
    else
        echo -e "${RED}✗${NC} Dataset vacío o corrupto"
        ((ERRORS++))
    fi
    
    # Verificar columnas
    HEADER=$(head -1 data/dataset_instagram_unmsm.csv)
    if [[ $HEADER == *"comentario"* ]] && [[ $HEADER == *"sentimiento"* ]]; then
        echo -e "${GREEN}✓${NC} Columnas correctas detectadas"
    else
        echo -e "${YELLOW}⚠${NC} Verificar columnas del dataset"
        ((WARNINGS++))
    fi
else
    echo -e "${RED}✗${NC} Dataset no encontrado (CRÍTICO)"
    ((ERRORS++))
fi

echo ""
echo "4. VERIFICANDO DEPENDENCIAS"
echo "---------------------------"

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python instalado: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python no encontrado"
    ((ERRORS++))
fi

# Verificar pip
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    echo -e "${GREEN}✓${NC} pip instalado: $PIP_VERSION"
else
    echo -e "${YELLOW}⚠${NC} pip no encontrado"
    ((WARNINGS++))
fi

# Verificar requirements.txt
if [ -f "requirements.txt" ]; then
    REQ_COUNT=$(wc -l < requirements.txt)
    echo -e "${GREEN}✓${NC} requirements.txt tiene $REQ_COUNT líneas"
    
    # Verificar dependencias críticas
    for pkg in "fastapi" "uvicorn" "pandas" "scikit-learn" "nltk"; do
        if grep -q "$pkg" requirements.txt; then
            echo -e "  ${GREEN}✓${NC} $pkg"
        else
            echo -e "  ${RED}✗${NC} $pkg falta"
            ((ERRORS++))
        fi
    done
fi

echo ""
echo "5. VERIFICANDO ESTRUCTURA DE DIRECTORIOS"
echo "-----------------------------------------"

test -d "app"
check "Directorio app/"

test -d "app/routes"
check "Directorio app/routes/"

test -d "app/services"
check "Directorio app/services/"

test -d "app/schemas"
check "Directorio app/schemas/"

test -d "data"
check "Directorio data/"

test -d "ml_models" || mkdir -p ml_models
check_warning "Directorio ml_models/"

echo ""
echo "6. VERIFICANDO GIT"
echo "------------------"

if command -v git &> /dev/null; then
    if git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Repositorio Git inicializado"
        
        # Verificar .gitignore
        if [ -f ".gitignore" ]; then
            echo -e "${GREEN}✓${NC} .gitignore existe"
        else
            echo -e "${YELLOW}⚠${NC} .gitignore no encontrado"
            ((WARNINGS++))
        fi
        
        # Verificar archivos sin commit
        if [ -n "$(git status --porcelain)" ]; then
            echo -e "${YELLOW}⚠${NC} Hay cambios sin commit"
            ((WARNINGS++))
        else
            echo -e "${GREEN}✓${NC} Todos los cambios están commitados"
        fi
    else
        echo -e "${YELLOW}⚠${NC} No es un repositorio Git"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠${NC} Git no instalado"
    ((WARNINGS++))
fi

echo ""
echo "7. VERIFICANDO CONFIGURACIÓN"
echo "----------------------------"

# Verificar que no haya credenciales hardcodeadas
if grep -r "password\|secret\|api_key" --include="*.py" app/ 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} Posibles credenciales hardcodeadas encontradas"
    ((WARNINGS++))
else
    echo -e "${GREEN}✓${NC} No se encontraron credenciales hardcodeadas"
fi

echo ""
echo "=================================================="
echo "RESUMEN"
echo "=================================================="
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ TODO CORRECTO - LISTO PARA DESPLEGAR${NC}"
    echo ""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ $WARNINGS ADVERTENCIAS${NC}"
    echo "Puedes desplegar, pero revisa las advertencias"
    echo ""
    exit 0
else
    echo -e "${RED}✗ $ERRORS ERRORES${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ $WARNINGS ADVERTENCIAS${NC}"
    fi
    echo ""
    echo "NO DESPLEGAR - Corrige los errores primero"
    echo ""
    exit 1
fi
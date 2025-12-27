#!/usr/bin/env python3
"""
Instalador Inteligente para Python 3.13
Detecta problemas y usa versiones compatibles
"""
import subprocess
import sys
import re

def run_command(cmd):
    """Ejecuta un comando y retorna éxito/fracaso"""
    print(f"🔧 Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr[:200]}")
        return False
    print("✅ Completado")
    return True

def get_python_version():
    """Obtiene versión mayor.menor de Python"""
    import sys
    return f"{sys.version_info.major}.{sys.version_info.minor}"

def fix_requirements_for_python313():
    """Corrige requirements.txt para Python 3.13"""
    print("\n" + "="*60)
    print("CORRIGIENDO requirements.txt PARA PYTHON 3.13")
    print("="*60)
    
    # Leer el archivo original
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Reemplazos necesarios para Python 3.13
    replacements = {
        'scipy==1.13.1': 'scipy>=1.17.0  # Python 3.13 requiere >=1.17.0',
        'scikit-learn==1.5.0': 'scikit-learn>=1.8.0  # Ya instalado',
        'pydantic==2.5.0': 'pydantic>=2.9.2  # Versión compatible con 3.13',
        'wordcloud==1.9.2': '# wordcloud==1.9.2  # COMENTADO: Problema con Python 3.13',
        'Cython==3.0.11': 'Cython>=3.0.0',
    }
    
    # Aplicar reemplazos
    new_lines = []
    for line in lines:
        original_line = line.strip()
        replaced = False
        
        for old, new in replacements.items():
            if old in line:
                new_lines.append(f"{new}\n")
                print(f"📝 Reemplazado: {old} -> {new.split('#')[0].strip()}")
                replaced = True
                break
        
        if not replaced:
            new_lines.append(line)
    
    # Escribir archivo corregido
    with open('requirements_fixed.txt', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("\n✅ Archivo corregido: requirements_fixed.txt")
    return 'requirements_fixed.txt'

def install_with_fallback(package_spec):
    """Instala un paquete con fallback si falla"""
    print(f"\n📦 Intentando instalar: {package_spec}")
    
    # Primero intento normal
    if run_command(f'pip install "{package_spec}"'):
        return True
    
    # Si falla, intentar sin dependencias
    print("🔄 Intentando sin dependencias...")
    if run_command(f'pip install "{package_spec}" --no-deps'):
        return True
    
    # Si aún falla, buscar alternativa
    print("🔍 Buscando versión alternativa...")
    package_name = package_spec.split('==')[0] if '==' in package_spec else package_spec.split('>=')[0]
    
    # Versiones alternativas conocidas para Python 3.13
    alternatives = {
        'scipy': 'scipy>=1.17.0',
        'pydantic': 'pydantic>=2.9.2',
        'wordcloud': '',  # Saltar este
        'scikit-learn': 'scikit-learn>=1.8.0',
    }
    
    if package_name in alternatives and alternatives[package_name]:
        print(f"🔄 Probando alternativa: {alternatives[package_name]}")
        return run_command(f'pip install "{alternatives[package_name]}"')
    
    print(f"⚠️  No se pudo instalar: {package_spec}")
    return False

def main():
    python_version = get_python_version()
    print(f"🐍 Python detectado: {python_version}")
    
    if python_version != "3.13":
        print("⚠️  Este script está optimizado para Python 3.13")
    
    # Paso 1: Corregir requirements.txt
    fixed_file = fix_requirements_for_python313()
    
    # Paso 2: Instalar en orden inteligente
    print("\n" + "="*60)
    print("INSTALACIÓN INTELIGENTE")
    print("="*60)
    
    # Orden de instalación CRÍTICO para Python 3.13
    critical_order = [
        # 1. Núcleo científico
        "numpy==1.26.4",
        "scipy>=1.17.0",
        "joblib==1.3.2",
        "threadpoolctl==3.4.0",
        
        # 2. ML principales (ya instalados)
        "scikit-learn>=1.8.0",
        "pandas>=2.2.1",
        "xgboost==2.0.2",
        "imbalanced-learn==0.11.0",
        
        # 3. FastAPI y dependencias
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "python-multipart==0.0.6",
        "pydantic>=2.9.2",
        "pydantic-settings>=2.1.0",
        
        # 4. NLP (excepto wordcloud)
        "nltk==3.8.1",
        "textblob==0.17.1",
        
        # 5. Visualización
        "matplotlib==3.8.3",
        "seaborn==0.13.2",
        "plotly==5.18.0",
    ]
    
    # Instalar en orden
    success_count = 0
    for package in critical_order:
        if package.strip() and not package.startswith('#'):
            if install_with_fallback(package):
                success_count += 1
    
    print(f"\n📊 Resumen: {success_count}/{len([p for p in critical_order if p.strip() and not p.startswith('#')])} paquetes instalados")
    
    # Paso 3: Instalar el resto desde archivo corregido
    print("\n" + "="*60)
    print("INSTALANDO RESTO DE DEPENDENCIAS")
    print("="*60)
    
    if run_command(f'pip install -r {fixed_file}'):
        print("✅ Todas las dependencias instaladas")
    else:
        print("⚠️  Algunas dependencias pueden faltar")
        print("   Intenta: pip install -r {fixed_file} --no-deps")
    
    # Paso 4: Verificar
    print("\n" + "="*60)
    print("VERIFICACIÓN FINAL")
    print("="*60)
    
    verification_code = """
import sys
print(f"Python: {sys.version}")

check_packages = [
    ('numpy', '1.26.4'),
    ('scipy', '1.17'),
    ('scikit-learn', '1.8'),
    ('pandas', '2.2'),
    ('fastapi', '0.104'),
    ('pydantic', '2.9'),
]

print("\\n✅ PAQUETES CRÍTICOS INSTALADOS:")
for pkg, ver in check_packages:
    try:
        mod = __import__(pkg.replace('-', '_'))
        actual_ver = getattr(mod, '__version__', 'N/A')
        if ver in actual_ver:
            print(f"  {pkg}: {actual_ver}")
        else:
            print(f"  ⚠️  {pkg}: {actual_ver} (esperaba {ver})")
    except ImportError:
        print(f"  ❌ {pkg}: NO INSTALADO")
"""
    
    run_command(f'python -c "{verification_code}"')

if __name__ == "__main__":
    main()

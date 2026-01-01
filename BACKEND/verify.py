"""
SCRIPT DE VERIFICACIÓN - Ejecutar en tu backend para diagnosticar
"""

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verificar_dataset(filepath: str):
    """
    Verifica que el dataset se esté cargando correctamente
    """
    print("\n" + "=" * 60)
    print("🔍 VERIFICACIÓN DE DATASET")
    print("=" * 60)
    
    # 1. Cargar CSV
    print(f"\n1️⃣ Cargando CSV desde: {filepath}")
    df = pd.read_csv(filepath, encoding="utf-8")
    print(f"   ✅ CSV cargado: {len(df)} filas, {len(df.columns)} columnas")
    print(f"   📋 Columnas originales: {list(df.columns)}")
    
    # 2. Identificar columnas
    print(f"\n2️⃣ Identificando columnas...")
    
    texto_col = None
    for col in df.columns:
        if any(k in col.lower() for k in ['texto', 'comentario', 'comment']):
            texto_col = col
            print(f"   ✅ Columna de texto encontrada: '{col}'")
            break
    
    sentimiento_col = None
    for col in df.columns:
        if any(k in col.lower() for k in ['sentimiento', 'sentiment', 'rating']):
            sentimiento_col = col
            print(f"   ✅ Columna de sentimiento encontrada: '{col}'")
            break
    
    if not texto_col:
        print(f"   ⚠️ No se encontró columna de texto, usando: {df.columns[0]}")
        texto_col = df.columns[0]
    
    if not sentimiento_col:
        print(f"   ⚠️ No se encontró columna de sentimiento")
    
    # 3. Renombrar
    print(f"\n3️⃣ Renombrando columnas...")
    df = df.rename(columns={
        texto_col: 'texto_comentario',
        sentimiento_col: 'sentimiento' if sentimiento_col else 'sentimiento_original'
    })
    print(f"   ✅ Columnas después del renombrado: {list(df.columns)}")
    
    # 4. Limpiar
    print(f"\n4️⃣ Limpiando datos...")
    print(f"   Antes de limpieza: {len(df)} filas")
    
    df = df.dropna(subset=['texto_comentario'])
    print(f"   Después de dropna: {len(df)} filas")
    
    df['texto_comentario'] = df['texto_comentario'].astype(str).str.strip()
    
    if 'sentimiento' not in df.columns:
        print(f"   ⚠️ Creando columna 'sentimiento' con valores 'Neutral'")
        df['sentimiento'] = 'Neutral'
    else:
        df['sentimiento'] = df['sentimiento'].astype(str).str.strip()
    
    # 5. Simplificar sentimientos
    print(f"\n5️⃣ Simplificando sentimientos...")
    print(f"   Valores únicos antes: {df['sentimiento'].unique()}")
    
    mapeo = {}
    for sent in df['sentimiento'].unique():
        sent_str = str(sent).lower()
        
        if any(p in sent_str for p in ['negativ', 'neg', 'mal', 'triste']):
            mapeo[sent] = 'Negativo'
        elif any(p in sent_str for p in ['neutral', 'neutr', 'inform']):
            mapeo[sent] = 'Neutral'
        elif any(p in sent_str for p in ['positiv', 'posit', 'buen', 'excel']):
            mapeo[sent] = 'Positivo'
        else:
            mapeo[sent] = 'Neutral'
    
    print(f"   Mapeo aplicado:")
    for original, nuevo in mapeo.items():
        print(f"      '{original}' -> '{nuevo}'")
    
    df['sentimiento'] = df['sentimiento'].map(mapeo).fillna('Neutral')
    print(f"   Valores únicos después: {df['sentimiento'].unique()}")
    
    # 6. Distribución final
    print(f"\n6️⃣ DISTRIBUCIÓN FINAL:")
    print(f"   {'='*50}")
    distribucion = df['sentimiento'].value_counts()
    total = len(df)
    
    for sentimiento, count in distribucion.items():
        porcentaje = (count / total) * 100
        print(f"   {sentimiento:12} : {count:6} ({porcentaje:5.2f}%)")
    
    print(f"   {'='*50}")
    print(f"   TOTAL        : {total:6}")
    print(f"   SUMA         : {distribucion.sum():6}")
    print(f"   ¿COINCIDEN?  : {'✅ SÍ' if distribucion.sum() == total else '❌ NO'}")
    print(f"   {'='*50}")
    
    # 7. Muestra de datos
    print(f"\n7️⃣ MUESTRA DE DATOS:")
    print(df[['texto_comentario', 'sentimiento']].head(5))
    
    print("\n" + "=" * 60)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 60 + "\n")
    
    return df


# Para ejecutar:
if __name__ == "__main__":
    # Reemplaza con tu ruta
    DATASET_PATH = "data/dataset_instagram_unmsm.csv"
    
    try:
        df_verificado = verificar_dataset(DATASET_PATH)
        print(f"\n✅ Dataset verificado correctamente")
        print(f"📊 Filas finales: {len(df_verificado)}")
        
    except Exception as e:
        print(f"\n❌ Error en verificación: {e}")
        import traceback
        traceback.print_exc()
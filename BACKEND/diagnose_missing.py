import pandas as pd
import numpy as np

def diagnosticar_perdida():
    """Encuentra los 64 comentarios perdidos"""
    
    print("\n" + "="*70)
    print("🔍 DIAGNÓSTICO DE COMENTARIOS PERDIDOS")
    print("="*70)
    
    # 1. Cargar el CSV original
    df_original = pd.read_csv("data/dataset_instagram_unmsm.csv", encoding="utf-8")
    print(f"\n📊 Dataset original: {len(df_original)} filas")
    
    # 2. Identificar columnas
    texto_col = None
    sent_col = None
    
    for col in df_original.columns:
        if any(k in col.lower() for k in ['texto', 'comentario', 'comment']):
            texto_col = col
        if any(k in col.lower() for k in ['sentimiento', 'sentiment']):
            sent_col = col
    
    print(f"📝 Columna texto: '{texto_col}'")
    print(f"😊 Columna sentimiento: '{sent_col}'")
    
    # 3. Analizar valores nulos
    print(f"\n❌ VALORES NULOS:")
    print(f"   Texto: {df_original[texto_col].isna().sum()}")
    print(f"   Sentimiento: {df_original[sent_col].isna().sum()}")
    
    # 4. Analizar valores vacíos
    print(f"\n⚪ VALORES VACÍOS (espacios/strings vacíos):")
    vacios_texto = df_original[texto_col].astype(str).str.strip().eq('').sum()
    vacios_sent = df_original[sent_col].astype(str).str.strip().eq('').sum()
    print(f"   Texto: {vacios_texto}")
    print(f"   Sentimiento: {vacios_sent}")
    
    # 5. Simular la limpieza que hace tu código
    df_limpio = df_original.copy()
    df_limpio = df_limpio.dropna(subset=[texto_col])
    
    print(f"\n🧹 Después de dropna({texto_col}): {len(df_limpio)} filas")
    print(f"   Perdidas: {len(df_original) - len(df_limpio)}")
    
    # 6. Ver qué sentimientos tienen los registros que se pierden
    if len(df_original) != len(df_limpio):
        perdidos = df_original[df_original[texto_col].isna()]
        print(f"\n🔴 REGISTROS PERDIDOS POR TEXTO NULO:")
        print(perdidos[[sent_col]].value_counts())
    
    # 7. Aplicar el mapeo de sentimientos
    mapeo = {}
    for sent in df_limpio[sent_col].unique():
        sent_str = str(sent).lower()
        
        if pd.isna(sent) or sent_str in ['nan', 'none', '']:
            mapeo[sent] = 'SIN_CLASIFICAR'
        elif any(p in sent_str for p in ['negativ', 'neg', 'mal', 'triste']):
            mapeo[sent] = 'Negativo'
        elif any(p in sent_str for p in ['neutral', 'neutr', 'inform', 'mixto']):
            mapeo[sent] = 'Neutral'
        elif any(p in sent_str for p in ['positiv', 'posit', 'buen', 'excel']):
            mapeo[sent] = 'Positivo'
        else:
            mapeo[sent] = 'SIN_CLASIFICAR'
    
    df_limpio['sentimiento_mapeado'] = df_limpio[sent_col].map(mapeo)
    
    # 8. Contar sin clasificar
    sin_clasificar = df_limpio['sentimiento_mapeado'].eq('SIN_CLASIFICAR').sum()
    print(f"\n⚠️ SENTIMIENTOS SIN CLASIFICAR: {sin_clasificar}")
    
    if sin_clasificar > 0:
        print("\n🔍 Valores sin clasificar:")
        sin_clase = df_limpio[df_limpio['sentimiento_mapeado'] == 'SIN_CLASIFICAR']
        print(sin_clase[sent_col].value_counts().head(20))
    
    # 9. Distribución final
    print(f"\n📊 DISTRIBUCIÓN FINAL:")
    dist = df_limpio['sentimiento_mapeado'].value_counts()
    print(dist)
    print(f"\nSUMA: {dist.sum()}")
    print(f"TOTAL ESPERADO: {len(df_original)}")
    print(f"DIFERENCIA: {len(df_original) - dist.sum()}")
    
    # 10. Encontrar los 64 perdidos
    diferencia = len(df_original) - dist[dist.index != 'SIN_CLASIFICAR'].sum()
    print(f"\n🎯 COMENTARIOS PERDIDOS: {diferencia}")
    
    if diferencia > 0:
        print("\n💡 POSIBLES CAUSAS:")
        print(f"   1. Textos nulos: {df_original[texto_col].isna().sum()}")
        print(f"   2. Sentimientos nulos: {df_original[sent_col].isna().sum()}")
        print(f"   3. Sentimientos sin mapeo: {sin_clasificar}")
        print(f"   4. Otros: {diferencia - df_original[texto_col].isna().sum() - sin_clasificar}")
    
    print("\n" + "="*70)
    
    return df_limpio

if __name__ == "__main__":
    try:
        df = diagnosticar_perdida()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
"""
TEST RÁPIDO - Ejecutar en la raíz del proyecto
Identifica el problema exacto con el dataset
"""
import pandas as pd
import sys

def test_dataset():
    """Test rápido del dataset"""
    print("\n" + "="*70)
    print("🔍 TEST RÁPIDO DE DATASET")
    print("="*70)
    
    try:
        # 1. Cargar CSV
        print("\n1️⃣ Cargando CSV...")
        df = pd.read_csv("data/dataset_instagram_unmsm.csv", encoding="utf-8")
        print(f"   ✅ Cargado: {len(df)} filas")
        print(f"   📋 Columnas: {list(df.columns)}")
        
        # 2. Verificar columnas críticas
        print("\n2️⃣ Verificando columnas críticas...")
        
        texto_col = None
        for col in df.columns:
            if 'texto' in col.lower() and 'comentario' in col.lower():
                texto_col = col
                print(f"   ✅ Columna texto: '{col}'")
                break
        
        if not texto_col:
            print(f"   ❌ No se encontró columna de texto")
            print(f"   Columnas disponibles: {list(df.columns)}")
            return False
        
        sent_col = None
        for col in df.columns:
            if 'sentimiento' in col.lower():
                sent_col = col
                print(f"   ✅ Columna sentimiento: '{col}'")
                break
        
        if not sent_col:
            print(f"   ❌ No se encontró columna de sentimiento")
            return False
        
        # 3. Verificar valores nulos
        print("\n3️⃣ Valores nulos:")
        print(f"   Texto: {df[texto_col].isna().sum()}")
        print(f"   Sentimiento: {df[sent_col].isna().sum()}")
        
        # 4. Probar el procesamiento básico
        print("\n4️⃣ Procesando...")
        
        # Renombrar
        df_test = df.rename(columns={
            texto_col: 'texto_comentario',
            sent_col: 'sentimiento'
        })
        
        # Rellenar nulos
        df_test['texto_comentario'] = df_test['texto_comentario'].fillna('[Sin texto]')
        df_test['sentimiento'] = df_test['sentimiento'].fillna('Neutral')
        
        # Convertir a string
        df_test['texto_comentario'] = df_test['texto_comentario'].astype(str).str.strip()
        df_test['sentimiento'] = df_test['sentimiento'].astype(str).str.strip()
        
        print(f"   ✅ Después de procesamiento: {len(df_test)} filas")
        
        # 5. Simplificar sentimientos
        print("\n5️⃣ Simplificando sentimientos...")
        
        def mapear(sent):
            s = str(sent).lower()
            if any(p in s for p in ['negativ', 'neg/', 'mal', 'trist']):
                return 'Negativo'
            elif any(p in s for p in ['positiv', 'posit/', 'buen', 'excel']):
                return 'Positivo'
            else:
                return 'Neutral'
        
        df_test['sentimiento'] = df_test['sentimiento'].apply(mapear)
        
        # 6. Distribución final
        print("\n6️⃣ DISTRIBUCIÓN FINAL:")
        print("   " + "="*50)
        
        dist = df_test['sentimiento'].value_counts()
        total = len(df_test)
        
        for sent, count in dist.items():
            pct = (count/total)*100
            print(f"   {sent:12} : {count:6} ({pct:5.2f}%)")
        
        print("   " + "="*50)
        print(f"   TOTAL        : {total:6}")
        print(f"   SUMA         : {dist.sum():6}")
        print(f"   ¿COINCIDEN?  : {'✅ SÍ' if dist.sum() == total else '❌ NO'}")
        print("   " + "="*50)
        
        if dist.sum() == total:
            print("\n✅ TEST EXITOSO - Dataset procesado correctamente")
            return True
        else:
            print("\n❌ TEST FALLIDO - Hay comentarios perdidos")
            return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_dataset()
    sys.exit(0 if success else 1)
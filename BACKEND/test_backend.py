"""
TEST BACKEND - Script de diagnóstico
Ejecutar: python test_backend.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_connection():
    """Test 1: Conexión básica"""
    print("\n" + "="*80)
    print("TEST 1: CONEXIÓN BÁSICA")
    print("="*80)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_report_endpoint():
    """Test 2: Endpoint de reportes"""
    print("\n" + "="*80)
    print("TEST 2: ENDPOINT DE REPORTES")
    print("="*80)
    
    try:
        payload = {
            "period": "current",
            "format": "json",
            "include_details": True
        }
        
        print(f"📤 Enviando request a: {BASE_URL}/api/reports/generate")
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/reports/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\n📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reporte generado exitosamente")
            print(f"\n📊 Resumen:")
            print(f"   - Success: {data.get('success')}")
            print(f"   - Title: {data.get('title')}")
            print(f"   - Period: {data.get('period_text')}")
            
            if 'summary' in data:
                summary = data['summary']
                print(f"\n📈 Summary:")
                print(f"   - Total: {summary.get('total_comments')}")
                print(f"   - Positivos: {summary.get('positive_percentage')}%")
                print(f"   - Negativos: {summary.get('negative_percentage')}%")
                print(f"   - Confianza: {summary.get('model_confidence')}%")
            
            if 'insights' in data:
                print(f"\n💡 Insights: {len(data['insights'])} encontrados")
                for insight in data['insights'][:3]:
                    print(f"   - {insight.get('title')}")
            
            if 'categories' in data:
                print(f"\n📁 Categorías: {len(data['categories'])} encontradas")
                for cat in data['categories'][:3]:
                    print(f"   - {cat.get('name')}: {cat.get('score')}%")
            
            print(f"\n✅ ESTRUCTURA COMPLETA:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:2000] + "...")
            
            return True
        else:
            print(f"❌ Error {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(traceback.format_exc())
        return False


def test_latest_report():
    """Test 3: Latest report"""
    print("\n" + "="*80)
    print("TEST 3: LATEST REPORT")
    print("="*80)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reports/latest", timeout=30)
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reporte obtenido")
            print(f"   Total: {data.get('summary', {}).get('total_comments')}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("\n" + "="*80)
    print("🔍 DIAGNÓSTICO DEL BACKEND - UNMSM SENTIMENT ANALYSIS")
    print("="*80)
    
    results = []
    
    # Test 1
    results.append(("Conexión básica", test_connection()))
    
    # Test 2
    results.append(("Generación de reporte", test_report_endpoint()))
    
    # Test 3
    results.append(("Latest report", test_latest_report()))
    
    # Resumen
    print("\n" + "="*80)
    print("📊 RESUMEN DE TESTS")
    print("="*80)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n📈 Total: {passed}/{total} tests pasados")
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("\n📌 PRÓXIMOS PASOS:")
        print("   1. El backend está funcionando correctamente")
        print("   2. Verifica que el frontend esté conectado a http://localhost:8000")
        print("   3. Revisa la consola del navegador (F12)")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")
        print("\n📌 ACCIONES:")
        print("   1. Verifica que el backend esté corriendo: uvicorn app.main:app --reload")
        print("   2. Verifica que el dataset esté cargado")
        print("   3. Revisa los logs del backend")


if __name__ == "__main__":
    main()
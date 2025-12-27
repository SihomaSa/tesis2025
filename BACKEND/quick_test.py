"""
PRUEBAS RÁPIDAS - Testing directo sin reentrenar
Útil para validar cambios en el diccionario
"""

import sys
from pathlib import Path

# Agregar path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.services.sentiment_analyzer import SentimentAnalyzer
from app.utils.config import settings

def quick_test():
    """Prueba rápida de casos críticos"""
    
    print("\n" + "="*70)
    print("🚀 PRUEBA RÁPIDA - Análisis de Sentimientos")
    print("="*70 + "\n")
    
    # Inicializar analizador
    analyzer = SentimentAnalyzer()
    
    # Intentar cargar modelo
    try:
        analyzer.load_model()
        print("✅ Modelo cargado\n")
    except FileNotFoundError:
        print("❌ Modelo no encontrado")
        print("💡 Ejecuta primero: python -m app.services.sentiment_service")
        print("   para entrenar el modelo\n")
        return
    
    # Casos de prueba críticos
    test_cases = [
        # NEUTRALES (los más problemáticos)
        ("y en el ranking internacional?", "Neutral"),
        ("Igual. Esta bien.", "Neutral"),
        ("Cuando es la próxima fecha?", "Neutral"),
        ("¿A qué hora?", "Neutral"),
        ("Link?", "Neutral"),
        ("Gracias", "Neutral"),
        
        # POSITIVOS (deben mantenerse)
        ("Orgulloso de nuestra alma mater ❤️", "Positivo"),
        ("Felicitaciones a la Decana de América! 👏", "Positivo"),
        ("Excelente trabajo 🔥", "Positivo"),
        ("Crack el cm", "Positivo"),
        ("Lo máximo! 🙌", "Positivo"),
        
        # NEGATIVOS (deben mantenerse)
        ("Ya pero que nos devuelvan el acceso a Scopus", "Negativo"),
        ("me robaron mi mochila", "Negativo"),
        ("pésima gestión", "Negativo"),
        ("No hay papel en los baños ps", "Negativo"),
        
        # MIXTOS/COMPLEJOS
        ("Siempre por sus alumnos, nunca por sus autoridades 👎", "Negativo"),
        ("A pesar de la gestión, siempre San Marquina ❤️", "Positivo"),
        ("Gracias Jeri 😮‍💨", "Negativo"),  # Sarcástico
    ]
    
    print("Casos de prueba:\n")
    
    correct = 0
    total = len(test_cases)
    
    for i, (text, expected) in enumerate(test_cases, 1):
        result = analyzer.analyze_single(text)
        predicted = result['sentiment']
        confidence = result['confidence']
        probs = result['probabilities']
        
        is_correct = predicted == expected
        if is_correct:
            correct += 1
        
        # Emojis de resultado
        status = "✅" if is_correct else "❌"
        sentiment_emoji = {"Positivo": "😊", "Negativo": "😡", "Neutral": "😐"}
        
        # Mostrar resultado
        print(f"{status} {i:2}. '{text[:50]}'")
        print(f"     Esperado: {expected:8} | Obtenido: {predicted:8} ({confidence:.1%})")
        
        if not is_correct:
            print(f"     📊 Neg={probs['negativo']:.2f}, Neu={probs['neutral']:.2f}, Pos={probs['positivo']:.2f}")
        print()
    
    # Resumen
    accuracy = correct / total
    print("="*70)
    print(f"📊 RESUMEN: {correct}/{total} correctos ({accuracy:.1%})")
    
    if accuracy >= 0.8:
        print("🎉 ¡Excelente! El modelo está funcionando bien")
    elif accuracy >= 0.6:
        print("⚠️  El modelo necesita ajustes")
    else:
        print("❌ El modelo necesita reentrenamiento")
    
    print("="*70 + "\n")
    
    # Análisis de distribución
    sentiment_counts = {"Positivo": 0, "Negativo": 0, "Neutral": 0}
    expected_counts = {"Positivo": 0, "Negativo": 0, "Neutral": 0}
    
    for _, expected in test_cases:
        expected_counts[expected] += 1
    
    print("\n📈 Distribución esperada vs obtenida:\n")
    
    for text, expected in test_cases:
        result = analyzer.analyze_single(text)
        sentiment_counts[result['sentiment']] += 1
    
    for sentiment in ["Positivo", "Neutral", "Negativo"]:
        exp = expected_counts[sentiment]
        got = sentiment_counts[sentiment]
        print(f"  {sentiment:10}: Esperado={exp:2}, Obtenido={got:2}")
    
    print()


def interactive_test():
    """Modo interactivo para probar textos"""
    
    print("\n" + "="*70)
    print("💬 MODO INTERACTIVO - Prueba tus propios textos")
    print("="*70 + "\n")
    
    analyzer = SentimentAnalyzer()
    
    try:
        analyzer.load_model()
        print("✅ Modelo cargado\n")
    except FileNotFoundError:
        print("❌ Modelo no encontrado. Entrena primero el modelo.\n")
        return
    
    print("Escribe textos para analizar (escribe 'salir' para terminar):\n")
    
    while True:
        text = input("➤ ").strip()
        
        if text.lower() in ['salir', 'exit', 'quit', '']:
            print("\n👋 ¡Hasta luego!\n")
            break
        
        result = analyzer.analyze_single(text)
        
        sentiment = result['sentiment']
        confidence = result['confidence']
        probs = result['probabilities']
        
        emoji = {"Positivo": "😊", "Negativo": "😡", "Neutral": "😐"}[sentiment]
        
        print(f"\n  {emoji} Sentimiento: {sentiment} ({confidence:.1%})")
        print(f"  📊 Probabilidades:")
        print(f"     Positivo: {probs['positivo']:.3f}")
        print(f"     Neutral:  {probs['neutral']:.3f}")
        print(f"     Negativo: {probs['negativo']:.3f}\n")


def batch_test_from_file(file_path: str):
    """Prueba casos desde un archivo CSV"""
    
    import pandas as pd
    
    print(f"\n📂 Cargando casos desde: {file_path}\n")
    
    analyzer = SentimentAnalyzer()
    
    try:
        analyzer.load_model()
    except FileNotFoundError:
        print("❌ Modelo no encontrado\n")
        return
    
    # Leer CSV
    try:
        df = pd.read_csv(file_path)
        
        if 'texto' not in df.columns or 'esperado' not in df.columns:
            print("❌ El CSV debe tener columnas: 'texto' y 'esperado'")
            return
        
        correct = 0
        results = []
        
        for idx, row in df.iterrows():
            text = row['texto']
            expected = row['esperado']
            
            result = analyzer.analyze_single(text)
            predicted = result['sentiment']
            
            is_correct = predicted == expected
            if is_correct:
                correct += 1
            
            results.append({
                'texto': text,
                'esperado': expected,
                'predicho': predicted,
                'correcto': is_correct,
                'confianza': result['confidence']
            })
        
        # Mostrar resultados
        results_df = pd.DataFrame(results)
        accuracy = correct / len(results)
        
        print(f"✅ Procesados {len(results)} casos")
        print(f"📊 Precisión: {accuracy:.1%}\n")
        
        # Guardar resultados
        output_file = file_path.replace('.csv', '_resultados.csv')
        results_df.to_csv(output_file, index=False)
        print(f"💾 Resultados guardados en: {output_file}\n")
        
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {file_path}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "interactive":
            interactive_test()
        elif mode == "file" and len(sys.argv) > 2:
            batch_test_from_file(sys.argv[2])
        else:
            print("\nUso:")
            print("  python quick_test.py              # Prueba rápida")
            print("  python quick_test.py interactive  # Modo interactivo")
            print("  python quick_test.py file <csv>   # Desde archivo\n")
    else:
        quick_test()
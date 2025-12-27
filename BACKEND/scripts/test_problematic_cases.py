# test_problematic_cases.py
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.services.sentiment_analyzer import SentimentAnalyzer
from colorama import init, Fore, Style

init(autoreset=True)

def test_problematic_cases():
    """Prueba específica de casos problemáticos"""
    print(f"\n{Fore.CYAN}🔍 PRUEBA ESPECÍFICA DE CASOS PROBLEMÁTICOS{Style.RESET_ALL}\n")
    
    analyzer = SentimentAnalyzer()
    analyzer.load_model()
    
    # Casos problemáticos identificados
    problematic_cases = [
        # Casos que deberían ser NEUTRAL pero son mal clasificados
        {'text': 'Gracias', 'expected': 'Neutral', 'current': 'Positivo'},
        {'text': 'Ok', 'expected': 'Neutral', 'current': 'Negativo'},
        {'text': 'Entendido', 'expected': 'Neutral', 'current': 'Negativo'},
        {'text': 'Ya', 'expected': 'Neutral', 'current': 'Negativo'},
        {'text': 'hasta donde sé, ya no figura', 'expected': 'Neutral', 'current': 'Negativo'},
        
        # Casos complejos/mixtos
        {'text': 'A pesar de la gestión pública, siempre San Marquina de corazón ❤️', 
         'expected': 'Positivo', 'current': 'Neutral'},
        {'text': 'Nro 1 a pesar de Jerí 🙌', 
         'expected': 'Positivo', 'current': 'Neutral'},
        {'text': 'Lo mejor de lo peor 😏😏', 
         'expected': 'Negativo', 'current': 'Positivo'},
        {'text': 'Lamentablemente viene retrocediendo hace décadas 😢', 
         'expected': 'Negativo', 'current': 'Positivo'},
        
        # Casos con ironía/sarcasmo
        {'text': 'La mitad de la vida universitaria es hacer cola😂', 
         'expected': 'Negativo', 'current': 'Positivo'},
    ]
    
    correct = 0
    total = len(problematic_cases)
    
    for case in problematic_cases:
        text = case['text']
        expected = case['expected']
        
        result = analyzer.analyze_single(text)
        predicted = result['sentiment']
        
        is_correct = predicted == expected
        if is_correct:
            correct += 1
        
        status = "✅" if is_correct else "❌"
        color = Fore.GREEN if is_correct else Fore.RED
        
        print(f"{color}{status} '{text}'")
        print(f"   Esperado: {expected} | Obtenido: {predicted}")
        print(f"   Confianza: {result['confidence']:.1%}")
        if not is_correct:
            print(f"   📊 Probabilidades: N={result['probabilities']['negativo']:.3f}, "
                  f"Ne={result['probabilities']['neutral']:.3f}, "
                  f"P={result['probabilities']['positivo']:.3f}")
        print()
    
    accuracy = correct / total
    print(f"\n{Fore.CYAN}📊 Resultados:{Style.RESET_ALL}")
    print(f"Correctos: {Fore.GREEN}{correct}/{total}{Style.RESET_ALL}")
    print(f"Precisión: {Fore.YELLOW}{accuracy:.1%}{Style.RESET_ALL}")
    
    if accuracy >= 0.7:
        print(f"\n{Fore.GREEN}🎉 ¡Mejora significativa en casos problemáticos!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}⚠️  Aún hay casos por mejorar{Style.RESET_ALL}")

if __name__ == "__main__":
    test_problematic_cases()
# test_casos_fallantes.py
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.services.sentiment_analyzer import SentimentAnalyzer
from colorama import init, Fore, Style

init(autoreset=True)

def analizar_casos_fallantes():
    """Analiza los 5 casos que aún fallan en test_sentiment.py"""
    print(f"\n{Fore.CYAN}🔍 ANÁLISIS DE CASOS FALLANTES RESTANTES{Style.RESET_ALL}\n")
    
    analyzer = SentimentAnalyzer()
    analyzer.load_model()
    
    casos_fallantes = [
        {
            'text': 'Con revisar anteriores rankings basta',
            'expected': 'Neutral',
            'problema': '"basta" puede sonar positivo pero es neutral aquí'
        },
        {
            'text': 'Súbanle el sueldo al de marketing',
            'expected': 'Positivo', 
            'problema': 'Petición/sugerencia positiva (apoyo a trabajador)'
        },
        {
            'text': 'Veremos si es arroz con pollo o seco con huesito. 😢',
            'expected': 'Negativo',
            'problema': 'Metáfora negativa + 😢 (expectativa vs realidad pobre)'
        },
        {
            'text': 'Rectorado? Es deber de la oficina de bienestar',
            'expected': 'Negativo',
            'problema': 'Pregunta retórica + crítica implícita a gestión'
        },
        {
            'text': 'pero depende del alumno/egresado mantener ese level',
            'expected': 'Neutral',
            'problema': '"pero depende" suena negativo pero es observación neutral'
        }
    ]
    
    correctos = 0
    for i, caso in enumerate(casos_fallantes, 1):
        texto = caso['text']
        esperado = caso['expected']
        
        resultado = analyzer.analyze_single(texto)
        obtenido = resultado['sentiment']
        
        if obtenido == esperado:
            correctos += 1
            icono = "✅"
            color = Fore.GREEN
        else:
            icono = "❌"
            color = Fore.RED
        
        print(f"{color}{icono} Caso {i}: '{texto}'")
        print(f"   Problema: {caso['problema']}")
        print(f"   Esperado: {esperado} | Obtenido: {obtenido}")
        print(f"   Confianza: {resultado['confidence']:.1%}")
        print(f"   Probabilidades: N={resultado['probabilities']['negativo']:.3f}, "
              f"Ne={resultado['probabilities']['neutral']:.3f}, "
              f"P={resultado['probabilities']['positivo']:.3f}")
        print()
    
    print(f"{Fore.CYAN}📊 Resultado: {correctos}/{len(casos_fallantes)} correctos "
          f"({correctos/len(casos_fallantes):.0%}){Style.RESET_ALL}")
    
    if correctos == len(casos_fallantes):
        print(f"{Fore.GREEN}🎉 ¡PERFECTO! Todos los casos corregidos{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Ejecuta 'python test_sentiment.py' para ver la mejora general{Style.RESET_ALL}")
    elif correctos >= 3:
        print(f"{Fore.GREEN}📈 ¡Buena mejora!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️  Aún necesita ajustes{Style.RESET_ALL}")

if __name__ == "__main__":
    analizar_casos_fallantes()
# test_mejoras_rapidas.py
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.services.sentiment_analyzer import SentimentAnalyzer
from colorama import init, Fore, Style

init(autoreset=True)

def probar_mejoras():
    print(f"\n{Fore.CYAN}🧪 PROBANDO MEJORAS EN CASOS PROBLEMÁTICOS{Style.RESET_ALL}\n")
    
    analyzer = SentimentAnalyzer()
    analyzer.load_model()
    
    casos_criticos = [
        ('hasta donde sé, ya no figura', 'Neutral'),
        ('A pesar de la gestión pública, siempre San Marquina de corazón ❤️', 'Positivo'),
        ('Nro 1 a pesar de Jerí 🙌', 'Positivo'),
        ('Lo mejor de lo peor 😏😏', 'Negativo'),
        ('La mitad de la vida universitaria es hacer cola😂', 'Negativo'),
    ]
    
    correctos = 0
    for texto, esperado in casos_criticos:
        resultado = analyzer.analyze_single(texto)
        obtenido = resultado['sentiment']
        
        if obtenido == esperado:
            correctos += 1
            icono = "✅"
            color = Fore.GREEN
        else:
            icono = "❌"
            color = Fore.RED
        
        print(f"{color}{icono} '{texto[:40]}...'")
        print(f"   Esperado: {esperado} | Obtenido: {obtenido}")
        print(f"   Confianza: {resultado['confidence']:.1%}")
        print()
    
    print(f"{Fore.CYAN}📊 Resultado: {correctos}/{len(casos_criticos)} correctos "
          f"({correctos/len(casos_criticos):.0%}){Style.RESET_ALL}")
    
    if correctos >= 4:
        print(f"{Fore.GREEN}🎉 ¡Mejora significativa!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️  Necesita más ajustes{Style.RESET_ALL}")

if __name__ == "__main__":
    probar_mejoras()
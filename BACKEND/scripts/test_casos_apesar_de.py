# test_casos_apesar_de.py
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.services.sentiment_analyzer import SentimentAnalyzer
from colorama import init, Fore, Style

init(autoreset=True)

def analizar_casos_apesar_de():
    """Análisis detallado de casos con 'a pesar de'"""
    print(f"\n{Fore.CYAN}🔍 ANÁLISIS DETALLADO: Casos 'A pesar de'{Style.RESET_ALL}\n")
    
    analyzer = SentimentAnalyzer()
    analyzer.load_model()
    
    casos = [
        'A pesar de la gestión pública, siempre San Marquina de corazón ❤️',
        'Nro 1 a pesar de Jerí 🙌',
        'A pesar de todo, sigue siendo la mejor',
        'A pesar de los problemas, me encanta mi universidad',
        'Siempre San Marcos a pesar de todo',
    ]
    
    for i, texto in enumerate(casos, 1):
        print(f"{Fore.YELLOW}{'─'*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Caso {i}: '{texto}'{Style.RESET_ALL}")
        
        resultado = analyzer.analyze_single(texto)
        
        # Mostrar features específicas
        features = resultado.get('features', {})
        
        print(f"\n📊 Resultado: {Fore.GREEN if resultado['sentiment'] == 'Positivo' else Fore.YELLOW if resultado['sentiment'] == 'Neutral' else Fore.RED}{resultado['sentiment']}{Style.RESET_ALL}")
        print(f"   Confianza: {resultado['confidence']:.1%}")
        print(f"   Probabilidades: N={resultado['probabilities']['negativo']:.3f}, "
              f"Ne={resultado['probabilities']['neutral']:.3f}, "
              f"P={resultado['probabilities']['positivo']:.3f}")
        
        print(f"\n🔍 Features importantes:")
        print(f"   pos_word_score: {features.get('pos_word_score', 0):.2f}")
        print(f"   neg_word_score: {features.get('neg_word_score', 0):.2f}")
        print(f"   emoji_score: {features.get('emoji_score', 0):.2f}")
        print(f"   sentiment_diff: {features.get('sentiment_diff', 0):.2f}")
        
        # Análisis manual
        texto_lower = texto.lower()
        
        if 'a pesar de' in texto_lower:
            print(f"\n💡 Contiene 'a pesar de'")
            
            # Verificar indicadores positivos
            indicadores_positivos = ['siempre', 'corazón', 'nro 1', 'mejor', 'encanta', '❤️', '🙌']
            encontrados = [ind for ind in indicadores_positivos if ind in texto_lower]
            
            if encontrados:
                print(f"   ✓ Tiene indicadores positivos: {', '.join(encontrados)}")
            
            # Verificar si tiene emojis positivos
            emojis_positivos = ['❤️', '💖', '🔥', '👏', '🙌', '🎉', '🥰']
            emojis_en_texto = [emoji for emoji in emojis_positivos if emoji in texto]
            
            if emojis_en_texto:
                print(f"   ✓ Tiene emojis positivos: {', '.join(emojis_en_texto)}")
        
        if 'siempre san' in texto_lower:
            print(f"   ✓ 'siempre San' es indicador positivo muy fuerte")
    
    print(f"\n{Fore.YELLOW}{'─'*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📋 RESUMEN:{Style.RESET_ALL}")
    print(f"Los casos con 'a pesar de' + indicadores positivos fuertes deberían ser 'Positivo'")
    print(f"Necesitamos ajustar las reglas para dar más peso a los indicadores positivos")

if __name__ == "__main__":
    analizar_casos_apesar_de()
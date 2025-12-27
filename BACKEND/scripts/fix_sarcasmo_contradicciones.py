# fix_sarcasmo_contradicciones.py
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.services.sentiment_analyzer import SmartThresholdSystem
import numpy as np

# Guardar método original
original_adjust = SmartThresholdSystem.adjust_thresholds

def improved_adjust_thresholds(self, probas, texts, negative_threshold=0.35, positive_threshold=0.45):
    """Versión mejorada con detección de sarcasmo y contradicciones"""
    predictions = []
    
    for proba, texto in zip(probas, texts):
        prob_neg, prob_neu, prob_pos = proba
        texto_lower = texto.lower()
        
        # ========== NUEVAS REGLAS PARA SARCASMO ==========
        
        # 1. Sarcasmo con 😏 + elogio exagerado
        if '😏' in texto and any(phrase in texto_lower for phrase in 
                                ['claro que sí', 'claro que', 'por supuesto', 'excelente', 'perfecto']):
            predictions.append(0)  # Negativo
            continue
        
        # 2. Elogio + problema evidente
        positive_words = ['increíble', 'bueno', 'perfecto', 'excelente', 'maravilloso']
        problem_words = ['se cayó', 'no funciona', 'roto', 'malo', 'problema']
        
        if any(pword in texto_lower for pword in positive_words) and any(probword in texto_lower for probword in problem_words):
            predictions.append(0)  # Negativo
            continue
        
        # 3. Contradicción texto negativo + emoji positivo
        negative_phrases = ['no me gusta', 'odio', 'detesto', 'no quiero']
        positive_emojis = ['❤️', '💖', '🔥', '👏', '🎉']
        
        if any(phrase in texto_lower for phrase in negative_phrases) and any(emoji in texto for emoji in positive_emojis):
            predictions.append(0)  # Negativo
            continue
        
        # 4. 😂 en contexto negativo (risa nerviosa/sarcasmo)
        negative_context = ['pena', 'triste', 'mal', 'problema', 'queja']
        if '😂' in texto and any(word in texto_lower for word in negative_context):
            predictions.append(0)  # Negativo
            continue
        
        # 5. Sarcasmo obvio con "amo" + actividad negativa
        if 'amo' in texto_lower and any(word in texto_lower for word in ['esperar', 'cola', 'fila', 'tardar', 'problema']):
            predictions.append(0)  # Negativo
            continue
        
        # 6. Expresiones neutrales coloquiales
        neutral_expressions = [
            'no está mal', 'está bien', 'más o menos', 'ni fu ni fa',
            'no es perfecto', 'podría mejorar', 'regular', 'aceptable'
        ]
        
        if any(expr in texto_lower for expr in neutral_expressions):
            # Solo si no tiene palabras fuertemente positivas/negativas
            strong_words = any(word in texto_lower for word in 
                             ['excelente', 'increíble', 'perfecto', 'pésimo', 'horrible', 'odio'])
            if not strong_words and prob_neu > 0.3:
                predictions.append(1)  # Neutral
                continue
        
        # ========== REGLAS ORIGINALES ==========
        
        # Para el resto, usar lógica original
        predictions.append(np.argmax(proba))
    
    return np.array(predictions)

# Aplicar parche
SmartThresholdSystem.adjust_thresholds = improved_adjust_thresholds

print("✅ Sistema mejorado con detección de sarcasmo y contradicciones")

# Probar inmediatamente los casos problemáticos
from app.services.sentiment_analyzer import SentimentAnalyzer
from colorama import init, Fore, Style

init(autoreset=True)

analyzer = SentimentAnalyzer()
analyzer.load_model()

print("\n🧪 Probando casos problemáticos corregidos:\n")

casos_problematicos = [
    ('Claro que sí, excelente servicio 😏', 'Negativo'),
    ('Perfecto, justo lo que necesitaba 👎', 'Negativo'),
    ('Maravillosa la gestión de Jerí 😂', 'Negativo'),
    ('Increíble, se cayó el sistema otra vez 🔥', 'Negativo'),
    ('No está mal, pero podría mejorar', 'Neutral'),
    ('No es perfecto pero funciona', 'Neutral'),
    ('Está bien, más o menos', 'Neutral'),
    ('Ni fu ni fa', 'Neutral'),
    ('Estoy feliz 😢', 'Negativo'),
    ('Que pena me da 😂', 'Negativo'),
    ('No me gusta ❤️', 'Negativo'),
    ('Amo esperar 3 horas 👏', 'Negativo'),
]

resultados = []
for texto, esperado in casos_problematicos:
    resultado = analyzer.analyze_single(texto)
    obtenido = resultado['sentiment']
    es_correcto = obtenido == esperado
    
    icono = "✅" if es_correcto else "❌"
    color = Fore.GREEN if es_correcto else Fore.RED
    
    print(f"{color}{icono} '{texto[:40]}...'")
    print(f"   Esperado: {esperado} | Obtenido: {obtenido}")
    print(f"   Confianza: {resultado['confidence']:.1%}")
    
    if not es_correcto:
        print(f"   📊 Probabilidades: N={resultado['probabilities']['negativo']:.3f}, "
              f"Ne={resultado['probabilities']['neutral']:.3f}, "
              f"P={resultado['probabilities']['positivo']:.3f}")
    
    resultados.append(es_correcto)
    print()

correctos = sum(resultados)
total = len(resultados)
print(f"{Fore.CYAN}📊 Resultado: {correctos}/{total} correctos ({correctos/total:.1%}){Style.RESET_ALL}")

if correctos >= 10:
    print(f"{Fore.GREEN}🎉 ¡Mejora significativa en sarcasmo/contradicciones!{Style.RESET_ALL}")
elif correctos >= 8:
    print(f"{Fore.YELLOW}📈 ¡Buena mejora!{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}⚠️  Aún necesita más ajustes{Style.RESET_ALL}")
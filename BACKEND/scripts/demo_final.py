# demo_final.py - Para mostrar en la defensa
from app.services.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()
analyzer.load_model()

ejemplos = [
    "Orgulloso de nuestra alma mater ❤️",
    "Lamentablemente viene retrocediendo 😢",
    "A pesar de todo, siempre San Marcos",
    "hacer cola😂 es lo peor",
    "Con revisar rankings basta"
]

print("DEMOSTRACIÓN DEL SISTEMA:")
for texto in ejemplos:
    resultado = analyzer.analyze_single(texto)
    print(f"📝 '{texto}'")
    print(f"   → {resultado['sentiment']} ({resultado['confidence']:.0%} confianza)")
    print()
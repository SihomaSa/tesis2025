# presentacion_demo.py - Para mostrar en vivo
from app.services.sentiment_analyzer import SentimentAnalyzer

print("DEMOSTRACIÓN EN VIVO - UNMSM Sentiment Analysis")
print("=" * 50)

analyzer = SentimentAnalyzer()
analyzer.load_model()

ejemplos = [
    "¡Orgulloso de mi San Marcos! ❤️",
    "Lamentable que hayan subido las pensiones 😢",
    "¿Cuándo mejorarán los baños?",
    "A pesar de todo, siempre Decana 🔥",
    "Gracias por la información"
]

for texto in ejemplos:
    resultado = analyzer.analyze_single(texto)
    print(f"\n📝 Usuario: '{texto}'")
    print(f"   🤖 Sistema: {resultado['sentiment']} ({resultado['confidence']:.0%} confianza)")
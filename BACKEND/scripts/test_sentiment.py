"""
SCRIPT DE PRUEBAS - UNMSM SENTIMENT ANALYSIS
Valida las mejoras del diccionario con casos reales
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.services.sentiment_analyzer import SentimentAnalyzer
from app.utils.config import settings
import pandas as pd
from typing import List, Dict
from colorama import init, Fore, Style

# Inicializar colorama para colores en consola
init(autoreset=True)

class SentimentTester:
    """Clase para realizar pruebas del sistema de análisis"""
    
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
        self.test_cases = self._load_test_cases()
        
    def _load_test_cases(self) -> List[Dict]:
        """Carga casos de prueba categorizados"""
        return [
            # ===== CASOS NEUTRALES (Deberían mejorar) =====
            {
                'category': 'NEUTRAL - Preguntas/Consultas',
                'cases': [
                    {'text': 'y en el ranking internacional?', 'expected': 'Neutral'},
                    {'text': 'Y en el ranking nacional?', 'expected': 'Neutral'},
                    {'text': 'Cuando es la próxima fecha?', 'expected': 'Neutral'},
                    {'text': '¿A qué hora se presentan?', 'expected': 'Neutral'},
                    {'text': 'Horario del open day por favor', 'expected': 'Neutral'},
                    {'text': 'Información?', 'expected': 'Neutral'},
                    {'text': 'Link?', 'expected': 'Neutral'},
                    {'text': 'dónde queda el centro de salud?', 'expected': 'Neutral'},
                ]
            },
            {
                'category': 'NEUTRAL - Afirmaciones simples',
                'cases': [
                    {'text': 'Igual. Esta bien.', 'expected': 'Neutral'},
                    {'text': 'hasta donde sé, ya no figura', 'expected': 'Neutral'},
                    {'text': 'Ok', 'expected': 'Neutral'},
                    {'text': 'Entendido', 'expected': 'Neutral'},
                    {'text': 'Gracias', 'expected': 'Neutral'},  # Agradecimiento simple
                    {'text': 'Ya', 'expected': 'Neutral'},
                ]
            },
            {
                'category': 'NEUTRAL - Opiniones balanceadas',
                'cases': [
                    {'text': 'Subjetivo. Un ranking oficial le daría algo de objetividad.', 'expected': 'Neutral'},
                    {'text': 'Con revisar anteriores rankings basta', 'expected': 'Neutral'},
                    {'text': 'Sería bacán que la Sunedu lo formalice.', 'expected': 'Positivo'},  # Esto sí es positivo
                ]
            },
            
            # ===== CASOS POSITIVOS (Deben mantenerse/mejorar) =====
            {
                'category': 'POSITIVO - Orgullo y Logros',
                'cases': [
                    {'text': 'Orgulloso de nuestra alma mater ❤️', 'expected': 'Positivo'},
                    {'text': 'Felicitaciones a la Decana de América! 👏', 'expected': 'Positivo'},
                    {'text': 'Excelente Decana de América. 👏👏👏', 'expected': 'Positivo'},
                    {'text': 'Orgullo sanmarquino 💪💪', 'expected': 'Positivo'},
                    {'text': 'Que orgullo, compaññero!!', 'expected': 'Positivo'},
                    {'text': 'Grande mi San Marcos 🔥', 'expected': 'Positivo'},
                    {'text': 'Felicidades muchachones', 'expected': 'Positivo'},
                    {'text': 'Bien merecido...vamos UNMSM', 'expected': 'Positivo'},
                ]
            },
            {
                'category': 'POSITIVO - Admiración',
                'cases': [
                    {'text': 'La verdadera inalcanzable 🔥', 'expected': 'Positivo'},
                    {'text': 'Crack el cm 🔥', 'expected': 'Positivo'},
                    {'text': 'Súbanle el sueldo al de marketing', 'expected': 'Positivo'},
                    {'text': 'Ese admin con Master of Puppets, un personaje de cultura musical fina 🔥✨', 'expected': 'Positivo'},
                    {'text': 'Lo máximo! 🙌', 'expected': 'Positivo'},
                    {'text': 'Eres un capo', 'expected': 'Positivo'},
                ]
            },
            {
                'category': 'POSITIVO - Celebración',
                'cases': [
                    {'text': 'Nro 1 a pesar de Jerí 🙌', 'expected': 'Positivo'},  # Mixto pero más positivo
                    {'text': 'JAJAJA', 'expected': 'Neutral'},  # Risa sola es neutral (puede ser sarcasmo)
                    {'text': 'No me sorprende 🔥', 'expected': 'Positivo'},
                    {'text': '🔥🔥🔥🔥🔥🔥❤️❤️', 'expected': 'Positivo'},
                    {'text': 'Siempre San Marcos. 👏🏻👏🏻👏🏻', 'expected': 'Positivo'},
                ]
            },
            
            # ===== CASOS NEGATIVOS (Deben mantenerse) =====
            {
                'category': 'NEGATIVO - Críticas',
                'cases': [
                    {'text': 'Ya pero que nos devuelvan el acceso a Scopus', 'expected': 'Negativo'},
                    {'text': 'Lamentablemente viene retrocediendo hace décadas 😢', 'expected': 'Negativo'},
                    {'text': 'Hemos bajado al 951-1000 y lo presumen', 'expected': 'Negativo'},
                    {'text': 'La mitad de la vida universitaria es hacer cola😂', 'expected': 'Negativo'},  # Queja con humor
                    {'text': 'Veremos si es arroz con pollo o seco con huesito. 😢', 'expected': 'Negativo'},
                ]
            },
            {
                'category': 'NEGATIVO - Gestión/Problemas',
                'cases': [
                    {'text': 'Rectorado? Es deber de la oficina de bienestar', 'expected': 'Negativo'},
                    {'text': 'Lástima que ya no sea la primera universidad del Perú', 'expected': 'Negativo'},
                    {'text': 'No hay papel en los baños ps', 'expected': 'Negativo'},
                    {'text': 'me robaron mi mochila', 'expected': 'Negativo'},
                    {'text': 'pésima gestión', 'expected': 'Negativo'},
                ]
            },
            
            # ===== CASOS MIXTOS/COMPLEJOS =====
            {
                'category': 'MIXTO - Contexto complejo',
                'cases': [
                    {'text': 'Siempre por sus alumnos, nunca por sus autoridades ni su gestión👎', 'expected': 'Negativo'},  # Crítica fuerte al final
                    {'text': 'A pesar de la gestión pública, siempre San Marquina de corazón ❤️', 'expected': 'Positivo'},  # Amor predomina
                    {'text': 'Lo mejor de lo peor 😏😏', 'expected': 'Negativo'},  # Sarcástico
                    {'text': 'Gracias Jeri 😮‍💨😮‍💨', 'expected': 'Negativo'},  # Sarcástico
                ]
            },
            
            # ===== CASOS ESPECÍFICOS DE TUS COMENTARIOS =====
            {
                'category': 'CASOS REALES - Problemáticos anteriormente',
                'cases': [
                    {'text': 'UNMSM tiene historia y prestigio a nivel nacional/internacional', 'expected': 'Positivo'},
                    {'text': 'pero depende del alumno/egresado mantener ese level', 'expected': 'Neutral'},
                    {'text': 'Para mí siempre es un orgullo presentarme como sanmarquina.', 'expected': 'Positivo'},
                    {'text': 'Es mi querida alma Mater ❤️', 'expected': 'Positivo'},
                    {'text': 'yo quierooo participar', 'expected': 'Positivo'},
                    {'text': 'Mi futura facultad', 'expected': 'Positivo'},
                ]
            },
        ]
    
    def run_tests(self, verbose: bool = True):
        """Ejecuta todas las pruebas"""
        print(f"\n{'='*80}")
        print(f"{Fore.CYAN}🧪 INICIANDO PRUEBAS DEL SISTEMA DE ANÁLISIS DE SENTIMIENTOS{Style.RESET_ALL}")
        print(f"{'='*80}\n")
        
        # Primero cargar o entrenar el modelo
        try:
            print(f"{Fore.YELLOW}📦 Cargando modelo...{Style.RESET_ALL}")
            self.analyzer.load_model()
            print(f"{Fore.GREEN}✅ Modelo cargado exitosamente{Style.RESET_ALL}\n")
        except FileNotFoundError:
            print(f"{Fore.YELLOW}⚠️  Modelo no encontrado. Entrenando nuevo modelo...{Style.RESET_ALL}")
            dataset_path = settings.DATA_DIR / settings.DATASET_FILE
            
            if not dataset_path.exists():
                print(f"{Fore.RED}❌ ERROR: Dataset no encontrado en {dataset_path}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 Por favor, coloca el dataset en: {dataset_path}{Style.RESET_ALL}")
                return
            
            self.analyzer.load_dataset(str(dataset_path))
            self.analyzer.train_model()
            self.analyzer.save_model()
            print(f"{Fore.GREEN}✅ Modelo entrenado y guardado{Style.RESET_ALL}\n")
        
        # Ejecutar pruebas por categoría
        total_tests = 0
        total_correct = 0
        results_by_category = {}
        
        for category_group in self.test_cases:
            category = category_group['category']
            cases = category_group['cases']
            
            print(f"\n{Fore.CYAN}{'─'*80}")
            print(f"📂 {category}")
            print(f"{'─'*80}{Style.RESET_ALL}\n")
            
            correct = 0
            total = len(cases)
            details = []
            
            for case in cases:
                text = case['text']
                expected = case['expected']
                
                # Analizar
                result = self.analyzer.analyze_single(text)
                predicted = result['sentiment']
                confidence = result['confidence']
                probabilities = result['probabilities']
                
                is_correct = predicted == expected
                
                if is_correct:
                    correct += 1
                    total_correct += 1
                
                total_tests += 1
                
                # Guardar detalles
                details.append({
                    'text': text,
                    'expected': expected,
                    'predicted': predicted,
                    'correct': is_correct,
                    'confidence': confidence,
                    'probabilities': probabilities
                })
                
                # Mostrar resultado
                if verbose or not is_correct:
                    status_icon = "✅" if is_correct else "❌"
                    status_color = Fore.GREEN if is_correct else Fore.RED
                    
                    print(f"{status_color}{status_icon} Texto: {text[:60]}...{Style.RESET_ALL}")
                    print(f"   Esperado: {Fore.YELLOW}{expected}{Style.RESET_ALL} | "
                          f"Obtenido: {status_color}{predicted}{Style.RESET_ALL} "
                          f"({confidence:.2%})")
                    
                    if not is_correct:
                        print(f"   📊 Probabilidades: "
                              f"Neg={probabilities['negativo']:.3f}, "
                              f"Neu={probabilities['neutral']:.3f}, "
                              f"Pos={probabilities['positivo']:.3f}")
                    print()
            
            # Resumen de categoría
            accuracy = correct / total if total > 0 else 0
            results_by_category[category] = {
                'correct': correct,
                'total': total,
                'accuracy': accuracy,
                'details': details
            }
            
            acc_color = Fore.GREEN if accuracy >= 0.8 else Fore.YELLOW if accuracy >= 0.6 else Fore.RED
            print(f"{acc_color}📊 Precisión en {category}: {correct}/{total} ({accuracy:.1%}){Style.RESET_ALL}\n")
        
        # Resumen general
        self._print_summary(total_correct, total_tests, results_by_category)
        
        return results_by_category
    
    def _print_summary(self, total_correct: int, total_tests: int, results: Dict):
        """Imprime resumen general de resultados"""
        overall_accuracy = total_correct / total_tests if total_tests > 0 else 0
        
        print(f"\n{'='*80}")
        print(f"{Fore.CYAN}📊 RESUMEN GENERAL{Style.RESET_ALL}")
        print(f"{'='*80}\n")
        
        print(f"Total de pruebas: {total_tests}")
        print(f"Correctas: {Fore.GREEN}{total_correct}{Style.RESET_ALL}")
        print(f"Incorrectas: {Fore.RED}{total_tests - total_correct}{Style.RESET_ALL}")
        
        acc_color = Fore.GREEN if overall_accuracy >= 0.8 else Fore.YELLOW if overall_accuracy >= 0.6 else Fore.RED
        print(f"\n{acc_color}🎯 PRECISIÓN TOTAL: {overall_accuracy:.1%}{Style.RESET_ALL}\n")
        
        # Desglose por sentimiento esperado
        print(f"{Fore.CYAN}📈 Precisión por Tipo de Sentimiento:{Style.RESET_ALL}\n")
        
        sentiment_stats = {'Positivo': {'correct': 0, 'total': 0},
                          'Negativo': {'correct': 0, 'total': 0},
                          'Neutral': {'correct': 0, 'total': 0}}
        
        for category, data in results.items():
            for detail in data['details']:
                expected = detail['expected']
                if expected in sentiment_stats:
                    sentiment_stats[expected]['total'] += 1
                    if detail['correct']:
                        sentiment_stats[expected]['correct'] += 1
        
        for sentiment, stats in sentiment_stats.items():
            if stats['total'] > 0:
                acc = stats['correct'] / stats['total']
                color = Fore.GREEN if acc >= 0.8 else Fore.YELLOW if acc >= 0.6 else Fore.RED
                icon = "😊" if sentiment == "Positivo" else "😡" if sentiment == "Negativo" else "😐"
                print(f"{icon} {sentiment:10} : {color}{stats['correct']:2}/{stats['total']:2} ({acc:.1%}){Style.RESET_ALL}")
        
        # Casos más problemáticos
        print(f"\n{Fore.YELLOW}⚠️  Categorías que necesitan mejora:{Style.RESET_ALL}\n")
        
        problem_categories = [(cat, data) for cat, data in results.items() 
                             if data['accuracy'] < 0.7]
        
        if problem_categories:
            for category, data in sorted(problem_categories, key=lambda x: x[1]['accuracy']):
                print(f"   • {category}: {data['accuracy']:.1%}")
        else:
            print(f"   {Fore.GREEN}✨ ¡Todas las categorías tienen >70% de precisión!{Style.RESET_ALL}")
        
        print(f"\n{'='*80}\n")
    
    def test_specific_cases(self, cases: List[str]):
        """Prueba casos específicos ingresados manualmente"""
        print(f"\n{Fore.CYAN}🔍 PRUEBA DE CASOS ESPECÍFICOS{Style.RESET_ALL}\n")
        
        for i, text in enumerate(cases, 1):
            result = self.analyzer.analyze_single(text)
            
            sentiment = result['sentiment']
            confidence = result['confidence']
            probabilities = result['probabilities']
            
            color = (Fore.GREEN if sentiment == "Positivo" else 
                    Fore.RED if sentiment == "Negativo" else 
                    Fore.YELLOW)
            
            print(f"{i}. {Fore.WHITE}'{text}'{Style.RESET_ALL}")
            print(f"   Sentimiento: {color}{sentiment}{Style.RESET_ALL} ({confidence:.2%})")
            print(f"   Probabilidades: Neg={probabilities['negativo']:.3f}, "
                  f"Neu={probabilities['neutral']:.3f}, Pos={probabilities['positivo']:.3f}")
            print()


def main():
    """Función principal"""
    print(f"\n{Fore.MAGENTA}╔═══════════════════════════════════════════════════════════════╗")
    print(f"║  SISTEMA DE PRUEBAS - UNMSM SENTIMENT ANALYSIS v3.1          ║")
    print(f"╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    tester = SentimentTester()
    
    # Ejecutar suite completa de pruebas
    results = tester.run_tests(verbose=False)  # verbose=False para solo mostrar errores
    
    # Pruebas adicionales personalizadas (opcional)
    print(f"\n{Fore.CYAN}💡 ¿Deseas probar casos adicionales? (s/n): {Style.RESET_ALL}", end='')
    
    # Para testing automático, comentar lo siguiente
    # response = input().strip().lower()
    # if response == 's':
    #     print("Ingresa los textos (Enter dos veces para terminar):\n")
    #     custom_cases = []
    #     while True:
    #         text = input("➤ ")
    #         if text.strip() == "":
    #             break
    #         custom_cases.append(text)
        
    #     if custom_cases:
    #         tester.test_specific_cases(custom_cases)
    
    print(f"\n{Fore.GREEN}✨ Pruebas completadas{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
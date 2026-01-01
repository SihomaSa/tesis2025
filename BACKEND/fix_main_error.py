import os

print("=== CORRIGIENDO ERROR EN main.py ===")

# Contenido corregido para main.py (solo la parte relevante)
main_correction = '''
# EN main.py, REEMPLAZA LAS LÍNEAS 84-90 CON ESTO:

        logger.info(f"Cargando dataset desde: {dataset_path}")
        try:
            # Cargar dataset usando el manager
            dataset_df = dataset_manager.load_dataset(dataset_path)
            
            if dataset_df is not None and not dataset_df.empty:
                # Pasar el dataset al sentiment analyzer
                sentiment_analyzer.df = dataset_df
                logger.info(f"[OK] Dataset cargado por manager: {len(dataset_df)} registros")
                
                # Intentar entrenar el modelo
                try:
                    logger.info("Cargando/entrenando modelo ML...")
                    sentiment_analyzer.load_or_train_model()
                    logger.info("✅ Modelo ML cargado/entrenado exitosamente")
                    
                    if hasattr(sentiment_analyzer, 'model_metadata') and sentiment_analyzer.model_metadata:
                        logger.info("✅ Sistema funcionará con modelo ML")
                    else:
                        logger.warning("[WARN] Modelo sin metadata, usando configuración básica")
                        logger.info("    Sistema funcionará con reglas heurísticas")
                        
                except Exception as model_error:
                    logger.error(f"[ERROR] Con modelo ML: {model_error}")
                    logger.info("    Sistema funcionará con reglas heurísticas")
            else:
                logger.error("[ERROR] Dataset vacío o None después de cargar")
                logger.info("    Sistema funcionará en modo demo")
                
        except Exception as e:
            logger.error(f"[ERROR] Cargando dataset: {e}")
            logger.info("    Sistema funcionará en modo demo")
'''

print("📋 Corrección para aplicar en main.py:")
print(main_correction)

# También necesitamos asegurar que sentiment_analyzer.py maneje bien el DataFrame
print("\n=== ACTUALIZANDO sentiment_analyzer.py ===")

sentiment_analyzer_content = '''
import pandas as pd
import numpy as np
import re
import joblib
import logging
import os
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Importaciones de scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Importación de SMOTE para balanceo
try:
    from imblearn.over_sampling import SMOTE
    HAS_SMOTE = True
except ImportError:
    HAS_SMOTE = False
    print("⚠️  SMOTE no disponible, continuando sin balanceo")

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Analizador de sentimientos para comentarios de Instagram UNMSM
    Versión simplificada y funcional
    """
    
    def __init__(self, model_path: str = None):
        self.df = None
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        self.model_path = model_path or "ml_models/sentiment_model.pkl"
        self.vectorizer_path = "ml_models/tfidf_vectorizer.pkl"
        
        # Mapeo SIMPLIFICADO de sentimientos
        self.sentiment_map = {
            'Negativo': 0,
            'Neutral': 1, 
            'Positivo': 2
        }
        self.reverse_sentiment_map = {v: k for k, v in self.sentiment_map.items()}
        
        # Metadata del modelo (IMPORTANTE: inicializar aquí)
        self.model_metadata = {}
        self.training_report = {}
        
        # Stopwords en español
        try:
            self.spanish_stopwords = set(stopwords.words('spanish'))
        except:
            self.spanish_stopwords = set()
            print("⚠️  No se pudieron cargar stopwords en español")
    
    def load_dataset(self, filepath: str) -> bool:
        """
        Carga el dataset desde un archivo CSV
        Retorna: True si se cargó correctamente, False si hubo error
        """
        try:
            logger.info(f"Cargando dataset desde: {filepath}")
            
            # Cargar dataset
            self.df = pd.read_csv(filepath, encoding="utf-8")
            logger.info(f"Dataset cargado: {len(self.df)} registros")
            
            # Mostrar columnas para debugging
            print(f"📊 Columnas en CSV: {list(self.df.columns)}")
            
            # Detectar y renombrar columnas automáticamente
            column_mapping = {}
            for col in self.df.columns:
                col_lower = col.lower()
                if 'texto' in col_lower or 'comment' in col_lower or 'comentario' in col_lower:
                    column_mapping[col] = 'texto_comentario'
                    print(f"📝 Detectado: {col} -> texto_comentario")
                elif 'sentimiento' in col_lower or 'sentiment' in col_lower or 'rating' in col_lower:
                    column_mapping[col] = 'sentimiento'
                    print(f"📝 Detectado: {col} -> sentimiento")
            
            if column_mapping:
                self.df = self.df.rename(columns=column_mapping)
                print("✅ Columnas renombradas para consistencia")
            
            # Verificar columnas requeridas
            required_cols = ['texto_comentario', 'sentimiento']
            missing_cols = [col for col in required_cols if col not in self.df.columns]
            
            if missing_cols:
                logger.warning(f"Columnas faltantes: {missing_cols}. Columnas disponibles: {list(self.df.columns)}")
                
                # Si no tenemos 'texto_comentario', buscar alternativa
                if 'texto_comentario' not in self.df.columns:
                    # Buscar cualquier columna que pueda contener texto
                    for col in self.df.columns:
                        if any(keyword in col.lower() for keyword in ['text', 'comment', 'coment', 'desc']):
                            self.df = self.df.rename(columns={col: 'texto_comentario'})
                            print(f"✅ Usando columna alternativa: {col} -> texto_comentario")
                            break
                
                if 'sentimiento' not in self.df.columns:
                    # Crear columna sentimiento por defecto (Neutral)
                    self.df['sentimiento'] = 'Neutral'
                    print("✅ Columna 'sentimiento' creada con valor 'Neutral' por defecto")
            
            # Simplificar sentimientos
            self._simplificar_sentimientos()
            
            # Limpiar datos
            self.clean_dataset()
            
            logger.info(f"Dataset procesado: {len(self.df)} comentarios válidos")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando dataset: {e}")
            self.df = None
            return False
    
    def _simplificar_sentimientos(self):
        """Simplifica las etiquetas de sentimiento a 3 categorías principales"""
        print("🔧 Simplificando categorías de sentimiento...")
        
        # Mapeo de categorías detalladas a categorías simples
        mapeo_simplificado = {}
        
        for sentimiento in self.df['sentimiento'].unique():
            sent_str = str(sentimiento).lower()
            
            if any(palabra in sent_str for palabra in ['negativo', 'negativa', 'neg', 'mal', 'triste', 'enojo', 'enoja', 'frustra', 'decep']):
                mapeo_simplificado[sentimiento] = 'Negativo'
            elif any(palabra in sent_str for palabra in ['neutral', 'neutro', 'informa', 'consulta', 'pregunta', 'duda']):
                mapeo_simplificado[sentimiento] = 'Neutral'
            elif any(palabra in sent_str for palabra in ['positivo', 'positiva', 'posit', 'bueno', 'buena', 'excelente', 'genial', 'feliz', 'alegr', 'orgullo', 'gracias']):
                mapeo_simplificado[sentimiento] = 'Positivo'
            else:
                # Por defecto, asignar Neutral
                mapeo_simplificado[sentimiento] = 'Neutral'
        
        # Aplicar mapeo
        self.df['sentimiento_original'] = self.df['sentimiento']
        self.df['sentimiento'] = self.df['sentimiento'].map(mapeo_simplificado)
        
        # Si algún sentimiento no fue mapeado, asignar Neutral
        self.df['sentimiento'] = self.df['sentimiento'].fillna('Neutral')
        
        # Mostrar distribución simplificada
        distribucion = self.df['sentimiento'].value_counts().to_dict()
        print(f"✅ Sentimientos simplificados: {distribucion}")
        
        return True
    
    def clean_dataset(self):
        """Limpia el dataset eliminando valores nulos y normalizando"""
        if self.df is None:
            return
        
        # Eliminar filas con valores nulos en columnas críticas
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['texto_comentario', 'sentimiento'])
        
        # Convertir a string y limpiar espacios
        self.df['texto_comentario'] = self.df['texto_comentario'].astype(str).str.strip()
        self.df['sentimiento'] = self.df['sentimiento'].astype(str).str.strip()
        
        # Capitalizar primera letra
        self.df['sentimiento'] = self.df['sentimiento'].str.capitalize()
        
        removed_count = initial_count - len(self.df)
        if removed_count > 0:
            logger.info(f"Se eliminaron {removed_count} filas con valores nulos")
        
        # Mostrar distribución final
        distribution = self.df['sentimiento'].value_counts().to_dict()
        logger.info(f"Distribución final: {distribution}")
    
    def clean_text(self, text: str) -> str:
        """Limpia el texto eliminando caracteres no deseados"""
        if not isinstance(text, str):
            return ""
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Eliminar URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Eliminar menciones (@usuario)
        text = re.sub(r'@\w+', '', text)
        
        # Eliminar hashtags
        text = re.sub(r'#\w+', '', text)
        
        # Eliminar caracteres especiales excepto letras, números y espacios
        text = re.sub(r'[^\\w\\sáéíóúñ]', ' ', text)
        
        # Eliminar números
        text = re.sub(r'\\d+', '', text)
        
        # Eliminar espacios múltiples
        text = re.sub(r'\\s+', ' ', text).strip()
        
        return text
    
    def preprocess_dataset(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Preprocesa el dataset para entrenamiento
        """
        try:
            logger.info("Preprocesando dataset...")
            
            # Verificar que tenemos datos
            if self.df is None or self.df.empty:
                raise ValueError("No hay dataset cargado")
            
            # Crear copia para no modificar el original
            df_combined = self.df.copy()
            
            # Limpiar texto
            df_combined['texto_limpio'] = df_combined['texto_comentario'].apply(self.clean_text)
            
            # Crear características adicionales
            df_combined['longitud_texto'] = df_combined['texto_limpio'].apply(len)
            df_combined['num_palabras'] = df_combined['texto_limpio'].apply(lambda x: len(x.split()))
            
            # Convertir sentimientos a numérico
            df_combined['sentimiento_numerico'] = df_combined['sentimiento'].map(self.sentiment_map)
            
            # Eliminar filas con sentimiento no mapeado
            df_combined = df_combined.dropna(subset=['sentimiento_numerico'])
            
            # Crear DataFrame de características
            clean_features_df = df_combined[['texto_limpio', 'longitud_texto', 'num_palabras']].copy()
            
            logger.info(f"Preprocesamiento completado: {len(df_combined)} comentarios")
            
            return df_combined, clean_features_df
            
        except Exception as e:
            logger.error(f"Error en preprocesamiento: {e}")
            raise
    
    def train_model(self):
        """Entrena el modelo de machine learning"""
        try:
            logger.info("Entrenando nuevo modelo...")
            
            # Preprocesar dataset
            df_combined, clean_features_df = self.preprocess_dataset()
            
            if df_combined.empty:
                logger.warning("No hay datos para entrenar el modelo")
                return False
            
            logger.info(f"Preprocesamiento completado: {len(df_combined)} comentarios")
            
            # Crear vectores TF-IDF
            logger.info("🔧 Creando vectores TF-IDF...")
            
            # Usar lista personalizada de stopwords en español
            custom_stopwords = list(self.spanish_stopwords) if self.spanish_stopwords else None
            
            self.vectorizer = TfidfVectorizer(
                max_features=500,
                min_df=2,
                max_df=0.95,
                stop_words=custom_stopwords,  # Usar lista en lugar de string
                ngram_range=(1, 2)
            )
            
            X_tfidf = self.vectorizer.fit_transform(clean_features_df['texto_limpio'])
            logger.info(f"{X_tfidf.shape[1]} características creadas")
            
            # Combinar características
            X_additional = clean_features_df[['longitud_texto', 'num_palabras']].values
            X_combined = np.hstack([X_tfidf.toarray(), X_additional])
            
            # Separar características y etiquetas
            X = X_combined
            y = df_combined['sentimiento_numerico'].values
            
            # Dividir en entrenamiento y prueba
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            logger.info(f"Train: {X_train.shape}, Test: {X_test.shape}")
            
            # Aplicar SMOTE para balanceo (si está disponible)
            if HAS_SMOTE and len(np.unique(y_train)) > 1:
                logger.info("Aplicando SMOTE para balanceo...")
                smote = SMOTE(random_state=42)
                X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)
                logger.info(f"Después de SMOTE - Train: {X_train_bal.shape}")
            else:
                if not HAS_SMOTE:
                    logger.warning("SMOTE no disponible, usando datos desbalanceados")
                X_train_bal, y_train_bal = X_train, y_train
            
            # Entrenar modelo
            logger.info("🔧 Entrenando modelo RandomForest...")
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=42,
                n_jobs=-1,
                class_weight='balanced'
            )
            
            self.model.fit(X_train_bal, y_train_bal)
            
            # Evaluar modelo
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, target_names=self.sentiment_map.keys())
            
            logger.info(f"✅ Modelo entrenado - Accuracy: {accuracy:.4f}")
            logger.info(f"Reporte de clasificación:\\n{report}")
            
            # Guardar modelo
            self.is_trained = True
            
            # Guardar en archivo
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            logger.info(f"Modelo guardado en: {self.model_path}")
            
            # Guardar vectorizador
            joblib.dump(self.vectorizer, self.vectorizer_path)
            logger.info(f"Vectorizador guardado en: {self.vectorizer_path}")
            
            self.model_metadata = {
                'accuracy': float(accuracy),
                'model_type': 'RandomForest',
                'training_samples': len(X_train_bal),
                'test_samples': len(X_test),
                'smote_used': HAS_SMOTE,
                'training_date': pd.Timestamp.now().isoformat()
            }
            
            self.training_report = report
            
            logger.info("✅ Entrenamiento completado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error durante el entrenamiento: {e}")
            self.is_trained = False
            return False
    
    def load_or_train_model(self):
        """Carga un modelo existente o entrena uno nuevo"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                logger.info("Cargando modelo existente...")
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                self.is_trained = True
                
                # Crear metadata básica si no existe
                if not self.model_metadata:
                    self.model_metadata = {
                        'model_type': 'RandomForest (cargado)',
                        'loading_date': pd.Timestamp.now().isoformat()
                    }
                
                logger.info("✅ Modelo cargado exitosamente")
                return True
            else:
                logger.info("No se encontró modelo existente, entrenando nuevo...")
                if self.df is not None and not self.df.empty:
                    return self.train_model()
                else:
                    logger.warning("No hay dataset disponible para entrenar")
                    return False
        except Exception as e:
            logger.error(f"Error cargando/entrenando modelo: {e}")
            self.is_trained = False
            return False
    
    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predice el sentimiento de un texto
        """
        try:
            if not self.is_trained or self.model is None:
                return {
                    'sentimiento': 'No determinado',
                    'confianza': 0.0,
                    'error': 'Modelo no entrenado'
                }
            
            # Limpiar texto
            clean_text = self.clean_text(text)
            
            # Extraer características
            if self.vectorizer:
                tfidf_features = self.vectorizer.transform([clean_text]).toarray()
                
                # Características adicionales
                length = len(clean_text)
                word_count = len(clean_text.split())
                
                # Combinar características
                features = np.hstack([tfidf_features, [[length, word_count]]])
                
                # Predecir
                prediction = self.model.predict(features)[0]
                probabilities = self.model.predict_proba(features)[0]
                
                # Obtener sentimiento
                sentiment = self.reverse_sentiment_map.get(prediction, 'Neutral')
                confidence = float(max(probabilities))
                
                return {
                    'sentimiento': sentiment,
                    'confianza': confidence,
                    'probabilidades': {
                        'Negativo': float(probabilities[0]),
                        'Neutral': float(probabilities[1]),
                        'Positivo': float(probabilities[2])
                    }
                }
            else:
                return {
                    'sentimiento': 'Error',
                    'confianza': 0.0,
                    'error': 'Vectorizador no disponible'
                }
                
        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            return {
                'sentimiento': 'Error',
                'confianza': 0.0,
                'error': str(e)
            }
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Obtiene información del dataset cargado"""
        if self.df is None or self.df.empty:
            return {'error': 'No hay dataset cargado'}
        
        return {
            'total_registros': int(len(self.df)),
            'distribucion_sentimientos': self.df['sentimiento'].value_counts().to_dict(),
            'columnas': list(self.df.columns),
            'muestra': self.df[['texto_comentario', 'sentimiento']].head(5).to_dict('records')
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Obtiene información del modelo"""
        return {
            'is_trained': self.is_trained,
            'model_metadata': self.model_metadata,
            'has_model': self.model is not None,
            'has_vectorizer': self.vectorizer is not None
        }
'''

# Guardar sentiment_analyzer.py actualizado
with open('app/services/sentiment_analyzer.py', 'w', encoding='utf-8') as f:
    f.write(sentiment_analyzer_content)

print("✅ sentiment_analyzer.py actualizado")

# 3. Crear un parche directo para main.py
print("\n=== CREANDO PARCHES PARA main.py ===")

# Primero, lee el main.py actual
main_path = 'main.py'
if os.path.exists(main_path):
    with open(main_path, 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Buscar la sección problemática (líneas alrededor de dataset loading)
    lines = main_content.split('\n')
    
    # Buscar la línea con "dataset_loaded ="
    for i, line in enumerate(lines):
        if 'dataset_loaded = dataset_manager.load_dataset' in line:
            print(f"📝 Línea problemática encontrada en línea {i+1}: {line}")
            
            # Reemplazar desde esa línea hacia adelante por unas cuantas líneas
            # Necesitamos reemplazar aproximadamente 5-10 líneas
            replacement = '''        logger.info(f"Cargando dataset desde: {dataset_path}")
        try:
            # Cargar dataset usando el manager
            dataset_df = dataset_manager.load_dataset(dataset_path)
            
            if dataset_df is not None and not dataset_df.empty:
                # Pasar el dataset al sentiment analyzer
                sentiment_analyzer.df = dataset_df
                logger.info(f"[OK] Dataset cargado por manager: {len(dataset_df)} registros")
                
                # Intentar entrenar el modelo
                try:
                    logger.info("Cargando/entrenando modelo ML...")
                    model_loaded = sentiment_analyzer.load_or_train_model()
                    
                    if model_loaded:
                        logger.info("✅ Modelo ML cargado/entrenado exitosamente")
                        
                        if hasattr(sentiment_analyzer, 'model_metadata') and sentiment_analyzer.model_metadata:
                            logger.info("✅ Sistema funcionará con modelo ML")
                        else:
                            logger.warning("[WARN] Modelo sin metadata, usando configuración básica")
                            logger.info("    Sistema funcionará con reglas heurísticas")
                    else:
                        logger.warning("[WARN] Modelo no disponible o no entrenado")
                        logger.info("    Sistema funcionará con reglas heurísticas")
                        
                except Exception as model_error:
                    logger.error(f"[ERROR] Con modelo ML: {model_error}")
                    logger.info("    Sistema funcionará con reglas heurísticas")
            else:
                logger.error("[ERROR] Dataset vacío o None después de cargar")
                logger.info("    Sistema funcionará en modo demo")
                
        except Exception as e:
            logger.error(f"[ERROR] Cargando dataset: {e}")
            logger.info("    Sistema funcionará en modo demo")'''
            
            # Reemplazar desde la línea actual hasta encontrar un break
            # Buscar el próximo "logger.info" o algo similar
            end_index = i
            for j in range(i, min(i+15, len(lines))):
                if 'logger.info(' in lines[j] and 'Dataset cargado' in lines[j]:
                    # Continuar buscando
                    continue
                elif 'logger.info(' in lines[j] or 'logger.error(' in lines[j]:
                    end_index = j
                    break
            
            # Reemplazar el bloque
            if end_index > i:
                lines[i:end_index] = [replacement]
            
            # Unir y guardar
            new_main_content = '\n'.join(lines)
            
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write(new_main_content)
            
            print("✅ main.py corregido")
            break
else:
    print("⚠️ main.py no encontrado")

print("\n✅ CORRECCIONES APLICADAS:")
print("1. sentiment_analyzer.py ahora retorna bool en load_dataset()")
print("2. main.py maneja correctamente el DataFrame vs bool")
print("3. model_metadata inicializado en constructor")

print("\n📋 Para reconstruir Docker:")
print("docker build -t adapted-api-fixed .")
print("docker run -p 8000:8000 adapted-api-fixed")

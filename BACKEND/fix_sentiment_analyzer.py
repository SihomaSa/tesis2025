import os

print("=== CORRIGIENDO SENTIMENT ANALYZER ===")

# Contenido actualizado del sentiment analyzer
sentiment_analyzer_content = '''
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List
import re
import joblib
import logging
import os
from collections import Counter
import nltk
from nltk.corpus import stopwords
from datetime import datetime

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
    Versión CORREGIDA con métodos que coinciden con las rutas
    """
    
    def __init__(self, model_path: str = None):
        self.df = None
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        self.model_path = model_path or "ml_models/sentiment_model.pkl"
        self.vectorizer_path = "ml_models/tfidf_vectorizer.pkl"
        
        # Mapeo de sentimientos
        self.sentiment_map = {
            'Negativo': 0,
            'Neutral': 1, 
            'Positivo': 2
        }
        self.reverse_sentiment_map = {v: k for k, v in self.sentiment_map.items()}
        
        # Metadata del modelo
        self.model_metadata = {}
        self.training_report = {}
        
        # Stopwords en español
        try:
            self.spanish_stopwords = set(stopwords.words('spanish'))
        except:
            self.spanish_stopwords = set()
            print("⚠️  No se pudieron cargar stopwords en español")
    
    def load_dataset(self, filepath: str) -> bool:
        """Carga el dataset desde CSV"""
        try:
            logger.info(f"Cargando dataset desde: {filepath}")
            self.df = pd.read_csv(filepath, encoding="utf-8")
            logger.info(f"Dataset cargado: {len(self.df)} registros")
            
            # Renombrar columnas automáticamente
            column_mapping = {}
            for col in self.df.columns:
                col_lower = col.lower()
                if 'texto' in col_lower or 'comment' in col_lower or 'comentario' in col_lower:
                    column_mapping[col] = 'texto_comentario'
                elif 'sentimiento' in col_lower or 'sentiment' in col_lower or 'rating' in col_lower:
                    column_mapping[col] = 'sentimiento'
            
            if column_mapping:
                self.df = self.df.rename(columns=column_mapping)
            
            # Si no tenemos las columnas necesarias, crearlas
            if 'texto_comentario' not in self.df.columns and len(self.df.columns) > 0:
                self.df = self.df.rename(columns={self.df.columns[0]: 'texto_comentario'})
            
            if 'sentimiento' not in self.df.columns:
                self.df['sentimiento'] = 'Neutral'
            
            # Simplificar sentimientos
            self._simplificar_sentimientos()
            
            # Limpiar datos
            self.clean_dataset()
            
            return True
            
        except Exception as e:
            logger.error(f"Error cargando dataset: {e}")
            return False
    
    def _simplificar_sentimientos(self):
        """Simplifica las etiquetas de sentimiento"""
        mapeo_simplificado = {}
        
        for sentimiento in self.df['sentimiento'].unique():
            sent_str = str(sentimiento).lower()
            
            if any(palabra in sent_str for palabra in ['negativo', 'negativa', 'neg', 'mal', 'triste', 'enojo']):
                mapeo_simplificado[sentimiento] = 'Negativo'
            elif any(palabra in sent_str for palabra in ['neutral', 'neutro', 'informa', 'consulta', 'pregunta']):
                mapeo_simplificado[sentimiento] = 'Neutral'
            elif any(palabra in sent_str for palabra in ['positivo', 'positiva', 'posit', 'bueno', 'buena', 'excelente']):
                mapeo_simplificado[sentimiento] = 'Positivo'
            else:
                mapeo_simplificado[sentimiento] = 'Neutral'
        
        self.df['sentimiento_original'] = self.df['sentimiento']
        self.df['sentimiento'] = self.df['sentimiento'].map(mapeo_simplificado).fillna('Neutral')
        
    def clean_dataset(self):
        """Limpia el dataset"""
        if self.df is None:
            return
        
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=['texto_comentario', 'sentimiento'])
        self.df['texto_comentario'] = self.df['texto_comentario'].astype(str).str.strip()
        self.df['sentimiento'] = self.df['sentimiento'].astype(str).str.strip().str.capitalize()
    
    def clean_text(self, text: str) -> str:
        """Limpia el texto"""
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        text = re.sub(r'[^\\w\\sáéíóúñ]', ' ', text)
        text = re.sub(r'\\d+', '', text)
        text = re.sub(r'\\s+', ' ', text).strip()
        
        return text
    
    def train_model(self):
        """Entrena el modelo"""
        try:
            logger.info("Entrenando modelo...")
            
            # Preparar datos
            self.df['texto_limpio'] = self.df['texto_comentario'].apply(self.clean_text)
            self.df['sentimiento_numerico'] = self.df['sentimiento'].map(self.sentiment_map)
            df_clean = self.df.dropna(subset=['sentimiento_numerico'])
            
            # TF-IDF
            self.vectorizer = TfidfVectorizer(
                max_features=500,
                min_df=2,
                max_df=0.95,
                stop_words=list(self.spanish_stopwords),
                ngram_range=(1, 2)
            )
            
            X_tfidf = self.vectorizer.fit_transform(df_clean['texto_limpio'])
            
            # Características adicionales
            df_clean['longitud'] = df_clean['texto_limpio'].apply(len)
            df_clean['palabras'] = df_clean['texto_limpio'].apply(lambda x: len(x.split()))
            X_features = df_clean[['longitud', 'palabras']].values
            
            # Combinar
            X = np.hstack([X_tfidf.toarray(), X_features])
            y = df_clean['sentimiento_numerico'].values
            
            # Dividir
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Balancear con SMOTE
            if HAS_SMOTE:
                smote = SMOTE(random_state=42)
                X_train, y_train = smote.fit_resample(X_train, y_train)
            
            # Entrenar
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=42,
                class_weight='balanced'
            )
            self.model.fit(X_train, y_train)
            
            # Evaluar
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Guardar
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.vectorizer, self.vectorizer_path)
            
            self.model_metadata = {
                'accuracy': float(accuracy),
                'model_type': 'RandomForest',
                'training_samples': len(X_train),
                'test_samples': len(X_test),
                'smote_used': HAS_SMOTE,
                'training_date': datetime.now().isoformat()
            }
            
            self.is_trained = True
            logger.info(f"✅ Modelo entrenado - Accuracy: {accuracy:.4f}")
            return True
            
        except Exception as e:
            logger.error(f"Error entrenando modelo: {e}")
            return False
    
    def load_or_train_model(self):
        """Carga o entrena modelo"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                self.is_trained = True
                logger.info("✅ Modelo cargado exitosamente")
                return True
            else:
                if self.df is not None and not self.df.empty:
                    return self.train_model()
                else:
                    logger.warning("No hay dataset para entrenar")
                    return False
        except Exception as e:
            logger.error(f"Error cargando/entrenando modelo: {e}")
            return False
    
    # === MÉTODOS QUE LAS RUTAS ESPERAN ===
    
    def analyze_single(self, text: str) -> Dict[str, Any]:
        """Analiza un comentario individual - método que las rutas esperan"""
        return self.predict(text)  # Usa el método predict existente
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analiza múltiples comentarios - método que las rutas esperan"""
        results = []
        for text in texts:
            try:
                result = self.predict(text)
                results.append(result)
            except Exception as e:
                results.append({
                    'comment': text,
                    'sentiment': 'Error',
                    'confidence': 0.0,
                    'error': str(e)
                })
        return results
    
    def predict(self, text: str) -> Dict[str, Any]:
        """Predice el sentimiento de un texto"""
        try:
            if not self.is_trained or self.model is None:
                return {
                    'comment': text,
                    'sentimiento': 'No determinado',
                    'confianza': 0.0,
                    'error': 'Modelo no entrenado',
                    'probabilities': {
                        'negativo': 0.33,
                        'neutral': 0.33,
                        'positivo': 0.33
                    },
                    'features': {},
                    'timestamp': datetime.now().isoformat()
                }
            
            # Limpiar texto
            clean_text = self.clean_text(text)
            
            # TF-IDF
            tfidf_vec = self.vectorizer.transform([clean_text]).toarray()
            
            # Características adicionales
            length = len(clean_text)
            word_count = len(clean_text.split())
            
            # Combinar
            features = np.hstack([tfidf_vec, [[length, word_count]]])
            
            # Predecir
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            
            # Resultado
            sentiment = self.reverse_sentiment_map.get(prediction, 'Neutral')
            confidence = float(max(probabilities))
            
            return {
                'comment': text,
                'sentimiento': sentiment,
                'confianza': confidence,
                'probabilities': {
                    'negativo': float(probabilities[0]),
                    'neutral': float(probabilities[1]),
                    'positivo': float(probabilities[2])
                },
                'features': {
                    'text_length': length,
                    'word_count': word_count,
                    'emoji_score': 0,
                    'pos_word_score': 0,
                    'neg_word_score': 0
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            return {
                'comment': text,
                'sentimiento': 'Error',
                'confianza': 0.0,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Obtiene información del dataset"""
        if self.df is None or self.df.empty:
            return {'error': 'No hay dataset cargado'}
        
        return {
            'total_comments': int(len(self.df)),
            'distribution': self.df['sentimiento'].value_counts().to_dict(),
            'columns': list(self.df.columns)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas - método que las rutas esperan"""
        return self.get_dataset_info()
    
    def save_model(self):
        """Guarda el modelo - método que el shutdown espera"""
        if self.model and self.vectorizer:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.vectorizer, self.vectorizer_path)
            logger.info("Modelo guardado")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Obtiene información del modelo"""
        return {
            'is_trained': self.is_trained,
            'model_metadata': self.model_metadata,
            'has_model': self.model is not None,
            'has_vectorizer': self.vectorizer is not None
        }
'''

# Guardar el archivo corregido
with open('app/services/sentiment_analyzer.py', 'w', encoding='utf-8') as f:
    f.write(sentiment_analyzer_content)

print("✅ sentiment_analyzer.py actualizado con los métodos correctos")
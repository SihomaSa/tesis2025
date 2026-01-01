"""
SentimentAnalyzer - ✅ VERSIÓN DEFINITIVA
Usa la misma lógica que quick_test.py que funciona correctamente
"""
import pandas as pd
import numpy as np
import re
import joblib
import logging
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from typing import Dict, Any, List, Tuple, Optional

try:
    from imblearn.over_sampling import SMOTE
    HAS_SMOTE = True
except ImportError:
    HAS_SMOTE = False

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """
    Analizador de sentimientos - UNMSM
    ✅ Versión que replica el test exitoso
    """
    
    def __init__(self, model_path: str = None):
        self.logger = logger
        self.df = None
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        self.model_path = model_path or "ml_models/sentiment_model.pkl"
        self.vectorizer_path = "ml_models/tfidf_vectorizer.pkl"
        
        self.sentiment_map = {
            'Negativo': 0,
            'Neutral': 1, 
            'Positivo': 2
        }
        self.reverse_sentiment_map = {v: k for k, v in self.sentiment_map.items()}
        
        self.model_metadata = {}
        self.training_report = {}
        self.dataset = None
        self.dataset_size = 0
        
        try:
            import nltk
            from nltk.corpus import stopwords
            self.spanish_stopwords = set(stopwords.words('spanish'))
        except:
            self.spanish_stopwords = set()
            logger.warning("No se pudieron cargar stopwords")
    
    def load_dataset(self, filepath: str) -> bool:
        """
        ✅ Carga dataset - Lógica exacta del test exitoso
        """
        try:
            logger.info(f"Cargando dataset desde: {filepath}")
            
            # 1. CARGAR CSV
            self.df = pd.read_csv(filepath, encoding="utf-8")
            initial_count = len(self.df)
            
            logger.info(f"📊 CSV cargado: {initial_count} filas")
            logger.info(f"📋 Columnas: {list(self.df.columns)}")
            
            # 2. IDENTIFICAR COLUMNAS (método robusto)
            texto_col = None
            for col in self.df.columns:
                col_clean = str(col).strip()
                if 'texto' in col_clean.lower() and 'comentario' in col_clean.lower():
                    texto_col = col_clean
                    logger.info(f"✅ Columna texto encontrada: '{col_clean}'")
                    break
            
            if not texto_col:
                raise ValueError(f"No se encontró columna de texto. Columnas: {list(self.df.columns)}")
            
            sent_col = None
            for col in self.df.columns:
                col_clean = str(col).strip()
                if 'sentimiento' in col_clean.lower():
                    sent_col = col_clean
                    logger.info(f"✅ Columna sentimiento encontrada: '{col_clean}'")
                    break
            
            if not sent_col:
                raise ValueError(f"No se encontró columna de sentimiento. Columnas: {list(self.df.columns)}")
            
            # 3. RENOMBRAR
            self.df = self.df.rename(columns={
                texto_col: 'texto_comentario',
                sent_col: 'sentimiento'
            })
            
            logger.info("✅ Columnas renombradas correctamente")
            
            # 4. VALORES NULOS
            null_textos = self.df['texto_comentario'].isna().sum()
            null_sentimientos = self.df['sentimiento'].isna().sum()
            
            logger.info(f"📊 Valores nulos - Texto: {null_textos}, Sentimiento: {null_sentimientos}")
            
            # 5. RELLENAR NULOS (exactamente como en el test)
            self.df['texto_comentario'] = self.df['texto_comentario'].fillna('[Sin texto]')
            self.df['sentimiento'] = self.df['sentimiento'].fillna('Neutral')
            
            # 6. CONVERTIR A STRING
            self.df['texto_comentario'] = self.df['texto_comentario'].astype(str).str.strip()
            self.df['sentimiento'] = self.df['sentimiento'].astype(str).str.strip()
            
            # 7. REEMPLAZAR STRINGS VACÍOS
            self.df.loc[self.df['texto_comentario'] == '', 'texto_comentario'] = '[Sin texto]'
            self.df.loc[self.df['sentimiento'].isin(['', 'nan', 'None', 'NaN']), 'sentimiento'] = 'Neutral'
            
            logger.info(f"✅ Procesamiento básico: {len(self.df)} filas")
            
            # 8. SIMPLIFICAR SENTIMIENTOS
            self._simplificar_sentimientos()
            
            # 9. VERIFICACIÓN FINAL
            distribucion = self.df['sentimiento'].value_counts()
            total = len(self.df)
            suma = distribucion.sum()
            
            logger.info("="*60)
            logger.info("📊 DISTRIBUCIÓN FINAL:")
            for sent, count in distribucion.items():
                pct = (count/total)*100
                logger.info(f"   {sent}: {count} ({pct:.2f}%)")
            logger.info(f"   TOTAL: {total}")
            logger.info(f"   SUMA: {suma}")
            logger.info(f"   ¿COINCIDEN? {'✅ SÍ' if suma == total else '❌ NO'}")
            logger.info("="*60)
            
            if suma != total:
                raise ValueError(f"CRÍTICO: suma={suma} vs total={total}")
            
            self.dataset = self.df
            self.dataset_size = len(self.df)
            
            logger.info(f"✅ Dataset cargado exitosamente: {total} comentarios")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cargando dataset: {e}", exc_info=True)
            return False
    
    def _simplificar_sentimientos(self):
        """
        ✅ Mapeo simple y efectivo (igual que el test)
        """
        logger.info("🔄 Simplificando sentimientos...")
        
        def mapear_sentimiento(sent: str) -> str:
            """Mapea sentimiento a Positivo/Neutral/Negativo"""
            s = str(sent).lower()
            
            # Negativos
            if any(p in s for p in ['negativ', 'neg/', 'mal', 'trist', 'frustrac', 
                                     'enojo', 'molest', 'decepc', 'critic', 'queja']):
                return 'Negativo'
            
            # Positivos
            elif any(p in s for p in ['positiv', 'posit/', 'buen', 'excel', 'alegr', 
                                       'feliz', 'orgullo', 'admirac', 'entusias']):
                return 'Positivo'
            
            # Por defecto: Neutral
            else:
                return 'Neutral'
        
        # Guardar original
        self.df['sentimiento_original'] = self.df['sentimiento'].copy()
        
        # Mapear
        self.df['sentimiento'] = self.df['sentimiento'].apply(mapear_sentimiento)
        
        # Verificar nulos
        if self.df['sentimiento'].isna().any():
            nulos = self.df['sentimiento'].isna().sum()
            logger.warning(f"⚠️ {nulos} nulos después del mapeo, rellenando...")
            self.df['sentimiento'] = self.df['sentimiento'].fillna('Neutral')
        
        logger.info(f"✅ Sentimientos simplificados: {self.df['sentimiento'].nunique()} únicos")
    
    def clean_text(self, text: str) -> str:
        """Limpia texto"""
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        text = re.sub(r'[^\w\sáéíóúñ]', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def preprocess_text(self, text: str) -> str:
        """Alias de clean_text"""
        return self.clean_text(text)
    
    def train_model(self):
        """Entrena modelo ML"""
        try:
            logger.info("🔧 Entrenando modelo...")
            
            if self.df is None or self.df.empty:
                logger.error("No hay dataset cargado")
                return False
            
            # Preparar datos
            self.df['texto_limpio'] = self.df['texto_comentario'].apply(self.clean_text)
            self.df['sentimiento_numerico'] = self.df['sentimiento'].map(self.sentiment_map)
            
            # Eliminar nulos
            df_clean = self.df.dropna(subset=['sentimiento_numerico']).copy()
            logger.info(f"Datos limpios: {len(df_clean)} comentarios")
            
            # TF-IDF
            self.vectorizer = TfidfVectorizer(
                max_features=500,
                min_df=2,
                max_df=0.95,
                stop_words=list(self.spanish_stopwords) if self.spanish_stopwords else None,
                ngram_range=(1, 2)
            )
            
            X_tfidf = self.vectorizer.fit_transform(df_clean['texto_limpio'])
            logger.info(f"TF-IDF: {X_tfidf.shape[1]} características")
            
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
            
            logger.info(f"Train: {X_train.shape}, Test: {X_test.shape}")
            
            # SMOTE
            if HAS_SMOTE:
                smote = SMOTE(random_state=42)
                X_train, y_train = smote.fit_resample(X_train, y_train)
                logger.info(f"Después de SMOTE: {X_train.shape}")
            
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
            
            logger.info(f"✅ Modelo entrenado - Accuracy: {accuracy:.4f}")
            
            # Guardar
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.vectorizer, self.vectorizer_path)
            
            self.model_metadata = {
                'accuracy': float(accuracy),
                'model_type': 'RandomForest',
                'training_samples': len(X_train),
                'test_samples': len(X_test),
                'training_date': datetime.now().isoformat()
            }
            
            self.is_trained = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Error entrenando: {e}", exc_info=True)
            return False
    
    def load_or_train_model(self):
        """Carga o entrena modelo"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                logger.info("Cargando modelo existente...")
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                self.is_trained = True
                logger.info("✅ Modelo cargado")
                return True
            else:
                logger.info("Entrenando nuevo modelo...")
                return self.train_model()
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return False
    
    def predict(self, text: str) -> Dict[str, Any]:
        """Predice sentimiento"""
        try:
            if not self.is_trained or self.model is None:
                return {
                    'comment': text,
                    'sentimiento': 'Neutral',
                    'confianza': 0.5,
                    'probabilities': {'negativo': 0.33, 'neutral': 0.33, 'positivo': 0.33},
                    'timestamp': datetime.now().isoformat()
                }
            
            clean_text = self.clean_text(text)
            tfidf_vec = self.vectorizer.transform([clean_text]).toarray()
            
            length = len(clean_text)
            word_count = len(clean_text.split())
            features = np.hstack([tfidf_vec, [[length, word_count]]])
            
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            
            sentiment = self.reverse_sentiment_map.get(prediction, 'Neutral')
            
            return {
                'comment': text,
                'sentimiento': sentiment,
                'confianza': float(max(probabilities)),
                'probabilities': {
                    'negativo': float(probabilities[0]),
                    'neutral': float(probabilities[1]),
                    'positivo': float(probabilities[2])
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {
                'comment': text,
                'sentimiento': 'Error',
                'confianza': 0.0,
                'error': str(e)
            }
    
    def analyze_single(self, text: str) -> Dict[str, Any]:
        """Alias de predict"""
        return self.predict(text)
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Info del dataset"""
        if self.df is None or self.df.empty:
            return {
                'error': 'No hay dataset',
                'total_comments': 0,
                'distribution': {},
                'percentages': {}
            }
        
        try:
            distribution = self.df['sentimiento'].value_counts().to_dict()
            total = len(self.df)
            
            percentages = {
                sentiment: round((count / total) * 100, 2)
                for sentiment, count in distribution.items()
            }
            
            return {
                'total_comments': int(total),
                'distribution': distribution,
                'percentages': percentages,
                'columns': list(self.df.columns)
            }
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {'error': str(e)}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Alias de get_dataset_info"""
        return self.get_dataset_info()
    
    def save_model(self):
        """Guarda modelo"""
        if self.model and self.vectorizer:
            try:
                os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
                joblib.dump(self.model, self.model_path)
                joblib.dump(self.vectorizer, self.vectorizer_path)
                logger.info("✅ Modelo guardado")
            except Exception as e:
                logger.error(f"❌ Error: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Info del modelo"""
        return {
            'is_trained': self.is_trained,
            'model_metadata': self.model_metadata,
            'has_model': self.model is not None,
            'has_vectorizer': self.vectorizer is not None
        }
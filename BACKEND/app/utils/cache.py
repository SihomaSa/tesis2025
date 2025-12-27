"""
Sistema de caché para optimización del análisis de sentimientos
Implementa caché multi-nivel con Redis + memoria
"""

import json
import pickle
import hashlib
import logging
from typing import Any, Optional, Union, Dict, List
from datetime import datetime, timedelta
from functools import wraps
import time

# Redis (si está disponible)
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

from app.utils.config import settings

logger = logging.getLogger(__name__)


class MultiLevelCache:
    """
    Sistema de caché multi-nivel con LRU y TTL
    Nivel 1: Memoria (LRU) - Más rápido
    Nivel 2: Redis - Persistente
    """
    
    def __init__(self, max_memory_size: int = 1000, redis_url: Optional[str] = None):
        """
        Inicializa el sistema de caché
        
        Args:
            max_memory_size: Máximo de elementos en caché de memoria
            redis_url: URL de conexión a Redis (opcional)
        """
        self.memory_cache = {}
        self.cache_order = []  # Para implementar LRU
        self.max_memory_size = max_memory_size
        
        # Inicializar Redis si está disponible
        self.redis_client = None
        self.use_redis = False
        
        if REDIS_AVAILABLE and (redis_url or settings.ENABLE_CACHE):
            try:
                redis_url = redis_url or settings.MONGODB_URL.replace('mongodb://', 'redis://')
                self.redis_client = redis.from_url(
                    redis_url,
                    decode_responses=False,
                    socket_timeout=5,
                    retry_on_timeout=True
                )
                # Probar conexión
                self.redis_client.ping()
                self.use_redis = True
                logger.info("✅ Redis cache habilitado")
            except Exception as e:
                logger.warning(f"⚠️  Redis no disponible, usando solo caché en memoria: {e}")
                self.redis_client = None
        else:
            logger.info("ℹ️  Redis no disponible, usando solo caché en memoria")
    
    def _generate_key(self, data: Any) -> str:
        """
        Genera una clave única para los datos
        
        Args:
            data: Datos a almacenar
            
        Returns:
            Clave hash MD5
        """
        if isinstance(data, str):
            data_str = data
        elif isinstance(data, (dict, list)):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
        
        return hashlib.md5(data_str.encode('utf-8')).hexdigest()
    
    def _clean_memory_cache(self):
        """Limpia el caché de memoria si excede el tamaño máximo"""
        if len(self.memory_cache) > self.max_memory_size:
            # Eliminar los elementos más antiguos (LRU)
            items_to_remove = len(self.memory_cache) - self.max_memory_size
            for key in self.cache_order[:items_to_remove]:
                if key in self.memory_cache:
                    del self.memory_cache[key]
            self.cache_order = self.cache_order[items_to_remove:]
            logger.debug(f"🧹 Limpiada caché de memoria, eliminados {items_to_remove} items")
    
    def _update_cache_order(self, key: str):
        """Actualiza el orden LRU"""
        if key in self.cache_order:
            self.cache_order.remove(key)
        self.cache_order.append(key)
    
    def set(self, key: str, value: Any, ttl: int = None, prefix: str = "cache"):
        """
        Almacena un valor en el caché
        
        Args:
            key: Clave del caché
            value: Valor a almacenar
            ttl: Time to Live en segundos
            prefix: Prefijo para la clave
        """
        if not settings.ENABLE_CACHE:
            return
        
        full_key = f"{prefix}:{key}"
        
        try:
            # Serializar valor
            serialized_value = pickle.dumps(value)
            
            # Almacenar en memoria (nivel 1)
            self.memory_cache[full_key] = {
                'value': serialized_value,
                'expires_at': datetime.now() + timedelta(seconds=ttl) if ttl else None
            }
            self._update_cache_order(full_key)
            self._clean_memory_cache()
            
            # Almacenar en Redis (nivel 2)
            if self.use_redis and self.redis_client:
                try:
                    if ttl:
                        self.redis_client.setex(full_key, ttl, serialized_value)
                    else:
                        self.redis_client.set(full_key, serialized_value)
                except Exception as e:
                    logger.warning(f"⚠️  Error almacenando en Redis: {e}")
            
            logger.debug(f"💾 Guardado en caché: {full_key} (TTL: {ttl}s)")
            
        except Exception as e:
            logger.error(f"❌ Error almacenando en caché: {e}")
    
    def get(self, key: str, prefix: str = "cache") -> Optional[Any]:
        """
        Obtiene un valor del caché
        
        Args:
            key: Clave del caché
            prefix: Prefijo para la clave
            
        Returns:
            Valor almacenado o None
        """
        if not settings.ENABLE_CACHE:
            return None
        
        full_key = f"{prefix}:{key}"
        
        try:
            # Intentar obtener de memoria (nivel 1)
            if full_key in self.memory_cache:
                cache_item = self.memory_cache[full_key]
                
                # Verificar expiración
                if cache_item['expires_at'] and cache_item['expires_at'] < datetime.now():
                    del self.memory_cache[full_key]
                    if full_key in self.cache_order:
                        self.cache_order.remove(full_key)
                    logger.debug(f"🗑️  Elemento expirado: {full_key}")
                    return None
                
                # Actualizar orden LRU
                self._update_cache_order(full_key)
                
                # Deserializar y retornar
                value = pickle.loads(cache_item['value'])
                logger.debug(f"⚡ Hit en caché de memoria: {full_key}")
                return value
            
            # Intentar obtener de Redis (nivel 2)
            if self.use_redis and self.redis_client:
                try:
                    redis_value = self.redis_client.get(full_key)
                    if redis_value:
                        # Almacenar en memoria para futuras consultas
                        value = pickle.loads(redis_value)
                        self.memory_cache[full_key] = {
                            'value': redis_value,
                            'expires_at': None  # No tenemos TTL exacto desde Redis
                        }
                        self._update_cache_order(full_key)
                        self._clean_memory_cache()
                        
                        logger.debug(f"🔗 Hit en caché Redis: {full_key}")
                        return value
                except Exception as e:
                    logger.warning(f"⚠️  Error obteniendo de Redis: {e}")
            
            logger.debug(f"❌ Miss en caché: {full_key}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo del caché: {e}")
            return None
    
    def delete(self, key: str, prefix: str = "cache") -> bool:
        """
        Elimina un valor del caché
        
        Args:
            key: Clave del caché
            prefix: Prefijo para la clave
            
        Returns:
            True si se eliminó correctamente
        """
        full_key = f"{prefix}:{key}"
        
        try:
            # Eliminar de memoria
            if full_key in self.memory_cache:
                del self.memory_cache[full_key]
                if full_key in self.cache_order:
                    self.cache_order.remove(full_key)
            
            # Eliminar de Redis
            if self.use_redis and self.redis_client:
                try:
                    self.redis_client.delete(full_key)
                except Exception as e:
                    logger.warning(f"⚠️  Error eliminando de Redis: {e}")
            
            logger.debug(f"🗑️  Eliminado del caché: {full_key}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error eliminando del caché: {e}")
            return False
    
    def clear(self, prefix: Optional[str] = None):
        """
        Limpia el caché
        
        Args:
            prefix: Prefijo para filtrar (opcional)
        """
        try:
            if prefix:
                # Limpiar solo elementos con prefijo específico
                keys_to_delete = [k for k in self.memory_cache.keys() if k.startswith(f"{prefix}:")]
                for key in keys_to_delete:
                    del self.memory_cache[key]
                
                # Limpiar de Redis
                if self.use_redis and self.redis_client:
                    try:
                        redis_keys = self.redis_client.keys(f"{prefix}:*")
                        if redis_keys:
                            self.redis_client.delete(*redis_keys)
                    except Exception as e:
                        logger.warning(f"⚠️  Error limpiando Redis: {e}")
                
                logger.info(f"🧹 Limpiado caché con prefijo: {prefix}")
            else:
                # Limpiar todo
                self.memory_cache.clear()
                self.cache_order.clear()
                
                if self.use_redis and self.redis_client:
                    try:
                        self.redis_client.flushdb()
                    except Exception as e:
                        logger.warning(f"⚠️  Error limpiando Redis DB: {e}")
                
                logger.info("🧹 Limpiado todo el caché")
                
        except Exception as e:
            logger.error(f"❌ Error limpiando caché: {e}")
    
    def exists(self, key: str, prefix: str = "cache") -> bool:
        """
        Verifica si una clave existe en el caché
        
        Args:
            key: Clave del caché
            prefix: Prefijo para la clave
            
        Returns:
            True si la clave existe
        """
        full_key = f"{prefix}:{key}"
        
        # Verificar en memoria
        if full_key in self.memory_cache:
            cache_item = self.memory_cache[full_key]
            if cache_item['expires_at'] and cache_item['expires_at'] < datetime.now():
                del self.memory_cache[full_key]
                return False
            return True
        
        # Verificar en Redis
        if self.use_redis and self.redis_client:
            try:
                return self.redis_client.exists(full_key) > 0
            except Exception as e:
                logger.warning(f"⚠️  Error verificando en Redis: {e}")
        
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del caché
        
        Returns:
            Diccionario con estadísticas
        """
        memory_stats = {
            'items': len(self.memory_cache),
            'max_size': self.max_memory_size,
            'memory_usage_percent': (len(self.memory_cache) / self.max_memory_size) * 100,
            'oldest_item': self.cache_order[0] if self.cache_order else None,
            'newest_item': self.cache_order[-1] if self.cache_order else None
        }
        
        redis_stats = {}
        if self.use_redis and self.redis_client:
            try:
                redis_info = self.redis_client.info()
                redis_stats = {
                    'connected': True,
                    'used_memory': redis_info.get('used_memory_human', 'N/A'),
                    'total_keys': redis_info.get('db0', {}).get('keys', 0),
                    'hit_rate': redis_info.get('keyspace_hits', 0) / 
                               max(redis_info.get('keyspace_misses', 0) + 
                                  redis_info.get('keyspace_hits', 1), 1) * 100
                }
            except Exception as e:
                redis_stats = {
                    'connected': False,
                    'error': str(e)
                }
        
        return {
            'memory': memory_stats,
            'redis': redis_stats,
            'use_redis': self.use_redis,
            'cache_enabled': settings.ENABLE_CACHE,
            'timestamp': datetime.now().isoformat()
        }
    
    def prefixed(self, prefix: str):
        """
        Retorna un cliente de caché con prefijo fijo
        
        Args:
            prefix: Prefijo para todas las operaciones
            
        Returns:
            Instancia de PrefixedCache
        """
        return PrefixedCache(self, prefix)


class PrefixedCache:
    """Cliente de caché con prefijo fijo"""
    
    def __init__(self, cache: MultiLevelCache, prefix: str):
        self.cache = cache
        self.prefix = prefix
    
    def set(self, key: str, value: Any, ttl: int = None):
        return self.cache.set(key, value, ttl, self.prefix)
    
    def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key, self.prefix)
    
    def delete(self, key: str) -> bool:
        return self.cache.delete(key, self.prefix)
    
    def exists(self, key: str) -> bool:
        return self.cache.exists(key, self.prefix)


def cache_result(ttl: int = 3600, key_prefix: str = "func", key_fields: Optional[List[str]] = None):
    """
    Decorador para cachear resultados de funciones
    
    Args:
        ttl: Time to Live en segundos
        key_prefix: Prefijo para las claves
        key_fields: Campos específicos para generar la clave (None = todos)
    
    Returns:
        Decorador
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Verificar si el caché está habilitado
            if not settings.ENABLE_CACHE:
                return func(*args, **kwargs)
            
            # Generar clave única para los argumentos
            cache_key_data = []
            
            if key_fields:
                # Usar solo campos específicos
                for field in key_fields:
                    if field in kwargs:
                        cache_key_data.append((field, kwargs[field]))
            else:
                # Usar todos los argumentos
                cache_key_data.extend([(f"arg{i}", arg) for i, arg in enumerate(args)])
                cache_key_data.extend(kwargs.items())
            
            # Generar clave hash
            key_str = json.dumps(cache_key_data, sort_keys=True)
            key_hash = hashlib.md5(key_str.encode()).hexdigest()
            cache_key = f"{key_prefix}:{func.__name__}:{key_hash}"
            
            # Intentar obtener del caché
            cached_result = get_cache(cache_key)
            if cached_result is not None:
                logger.debug(f"⚡ Resultado obtenido de caché: {cache_key}")
                return cached_result
            
            # Ejecutar función y cachear resultado
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Solo cachear si la ejecución tardó más de cierto tiempo
            # (para no cachear funciones muy rápidas)
            if execution_time > 0.1:  # 100ms
                set_cache(cache_key, result, ttl)
                logger.debug(f"💾 Resultado cacheado: {cache_key} ({execution_time:.3f}s)")
            
            return result
        
        return wrapper
    return decorator


def cache_invalidate(key_pattern: str, prefix: str = "cache"):
    """
    Decorador para invalidar caché después de una operación
    
    Args:
        key_pattern: Patrón de claves a invalidar (puede contener *)
        prefix: Prefijo para las claves
    
    Returns:
        Decorador
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Invalidar caché
            try:
                # Obtener instancia del caché
                cache = get_cache_instance()
                if cache:
                    if '*' in key_pattern:
                        # Buscar todas las claves que coincidan con el patrón
                        if hasattr(cache, 'redis_client') and cache.redis_client:
                            keys = cache.redis_client.keys(f"{prefix}:{key_pattern}")
                            if keys:
                                cache.redis_client.delete(*keys)
                                logger.debug(f"🗑️  Invalidadas {len(keys)} claves: {key_pattern}")
                    else:
                        # Invalidar clave específica
                        cache.delete(key_pattern, prefix)
                        logger.debug(f"🗑️  Invalidada clave: {prefix}:{key_pattern}")
            except Exception as e:
                logger.warning(f"⚠️  Error invalidando caché: {e}")
            
            return result
        
        return wrapper
    return decorator


# Instancia global del caché
_cache_instance = None


def get_cache_instance() -> Optional[MultiLevelCache]:
    """
    Obtiene la instancia global del caché (Singleton)
    
    Returns:
        Instancia de MultiLevelCache
    """
    global _cache_instance
    
    if _cache_instance is None:
        try:
            _cache_instance = MultiLevelCache(
                max_memory_size=settings.RATE_LIMIT_REQUESTS * 10,  # 10x el rate limit
                redis_url=settings.MONGODB_URL.replace('mongodb://', 'redis://')
            )
            logger.info("✅ Sistema de caché inicializado")
        except Exception as e:
            logger.error(f"❌ Error inicializando caché: {e}")
            _cache_instance = MultiLevelCache(max_memory_size=1000)  # Fallback
    
    return _cache_instance


def get_cache(key: str, prefix: str = "cache") -> Optional[Any]:
    """
    Función auxiliar para obtener del caché
    
    Args:
        key: Clave del caché
        prefix: Prefijo para la clave
    
    Returns:
        Valor del caché o None
    """
    cache = get_cache_instance()
    if cache:
        return cache.get(key, prefix)
    return None


def set_cache(key: str, value: Any, ttl: int = None, prefix: str = "cache"):
    """
    Función auxiliar para almacenar en el caché
    
    Args:
        key: Clave del caché
        value: Valor a almacenar
        ttl: Time to Live en segundos
        prefix: Prefijo para la clave
    """
    cache = get_cache_instance()
    if cache:
        cache.set(key, value, ttl, prefix)


def delete_cache(key: str, prefix: str = "cache") -> bool:
    """
    Función auxiliar para eliminar del caché
    
    Args:
        key: Clave del caché
        prefix: Prefijo para la clave
    
    Returns:
        True si se eliminó correctamente
    """
    cache = get_cache_instance()
    if cache:
        return cache.delete(key, prefix)
    return False


def clear_cache(prefix: Optional[str] = None):
    """
    Función auxiliar para limpiar el caché
    
    Args:
        prefix: Prefijo para filtrar (opcional)
    """
    cache = get_cache_instance()
    if cache:
        cache.clear(prefix)


def get_cache_stats() -> Dict[str, Any]:
    """
    Función auxiliar para obtener estadísticas del caché
    
    Returns:
        Diccionario con estadísticas
    """
    cache = get_cache_instance()
    if cache:
        return cache.get_stats()
    return {}


# Cachés específicos para diferentes tipos de datos
analysis_cache = None
model_cache = None
dataset_cache = None


def get_analysis_cache():
    """Obtiene caché específico para análisis"""
    global analysis_cache
    if analysis_cache is None:
        cache = get_cache_instance()
        if cache:
            analysis_cache = cache.prefixed("analysis")
    return analysis_cache


def get_model_cache():
    """Obtiene caché específico para modelos"""
    global model_cache
    if model_cache is None:
        cache = get_cache_instance()
        if cache:
            model_cache = cache.prefixed("model")
    return model_cache


def get_dataset_cache():
    """Obtiene caché específico para datasets"""
    global dataset_cache
    if dataset_cache is None:
        cache = get_cache_instance()
        if cache:
            dataset_cache = cache.prefixed("dataset")
    return dataset_cache


# Ejemplo de uso en los servicios
if __name__ == "__main__":
    # Ejemplo de uso básico
    set_cache("test_key", {"data": "test_value"}, ttl=60)
    
    cached_value = get_cache("test_key")
    print(f"Valor cacheado: {cached_value}")
    
    # Ejemplo con decorador
    @cache_result(ttl=300, key_fields=["comment"])
    def analyze_with_cache(comment: str, include_details: bool = True):
        print(f"Analizando: {comment}")
        return {"sentiment": "Positivo", "confidence": 0.85}
    
    # Primera llamada (cache miss)
    result1 = analyze_with_cache("Excelente servicio!")
    
    # Segunda llamada con mismo parámetro (cache hit)
    result2 = analyze_with_cache("Excelente servicio!")
    
    # Estadísticas del caché
    stats = get_cache_stats()
    print(f"\nEstadísticas del caché: {json.dumps(stats, indent=2, default=str)}")
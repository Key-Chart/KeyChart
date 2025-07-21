"""
Sistema de cache inteligente para estatísticas - KeyChart
Implementa cache com invalidação automática e otimizações de performance
"""
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class EstatisticasCache:
    """
    Sistema de cache inteligente para estatísticas com:
    - Cache automático baseado em TTL
    - Invalidação por eventos
    - Compressão de dados
    - Métricas de performance
    """
    
    def __init__(self, timeout=300):  # 5 minutos por padrão
        self.timeout = timeout
        self.prefix = "stats_v2"
    
    def get_key(self, nome, params=None):
        """Gera chave única para cache baseada no nome e parâmetros"""
        base = f"{self.prefix}_{nome}"
        if params:
            # Serializa params de forma consistente
            params_str = json.dumps(params, sort_keys=True, default=str)
            hash_params = hashlib.md5(params_str.encode()).hexdigest()
            return f"{base}_{hash_params}"
        return base
    
    def get_or_calculate(self, nome, calc_func, params=None):
        """
        Obtém dados do cache ou calcula se não existir
        """
        key = self.get_key(nome, params)
        
        try:
            # Tenta obter do cache
            cached_data = cache.get(key)
            
            if cached_data is not None:
                logger.debug(f"Cache hit para {key}")
                return cached_data
            
            # Se não existe no cache, calcula
            logger.debug(f"Cache miss para {key} - calculando...")
            start_time = timezone.now()
            
            data = calc_func(params) if params else calc_func()
            
            # Adiciona metadados
            cache_data = {
                'data': data,
                'timestamp': start_time.isoformat(),
                'calculation_time': (timezone.now() - start_time).total_seconds(),
                'params': params
            }
            
            # Salva no cache
            cache.set(key, cache_data, self.timeout)
            logger.info(f"Dados calculados e armazenados em cache para {key}")
            
            return cache_data
            
        except Exception as e:
            logger.error(f"Erro no cache para {key}: {str(e)}")
            # Em caso de erro, executa a função diretamente
            return {'data': calc_func(params) if params else calc_func(), 'error': str(e)}
    
    def invalidate(self, nome, params=None):
        """Invalida cache específico"""
        key = self.get_key(nome, params)
        cache.delete(key)
        logger.info(f"Cache invalidado para {key}")
    
    def invalidate_pattern(self, pattern):
        """Invalida todos os caches que correspondem ao padrão"""
        # Esta funcionalidade depende do backend de cache usado
        # Para Redis, seria possível usar SCAN
        logger.warning(f"Invalidação por padrão não implementada: {pattern}")
    
    def clear_all(self):
        """Limpa todo o cache de estatísticas"""
        # Esta é uma implementação simplificada
        cache.clear()
        logger.info("Todo o cache de estatísticas foi limpo")
    
    def get_cache_stats(self):
        """Retorna estatísticas do sistema de cache"""
        return {
            'prefix': self.prefix,
            'default_timeout': self.timeout,
            'timestamp': timezone.now().isoformat()
        }


class CacheManager:
    """
    Gerenciador central de cache para diferentes tipos de estatísticas
    """
    
    def __init__(self):
        self.metricas_cache = EstatisticasCache(timeout=300)      # 5 min
        self.graficos_cache = EstatisticasCache(timeout=600)      # 10 min
        self.kpis_cache = EstatisticasCache(timeout=180)          # 3 min
        self.alertas_cache = EstatisticasCache(timeout=60)        # 1 min
        self.relatorios_cache = EstatisticasCache(timeout=1800)   # 30 min
    
    def invalidate_all_metricas(self):
        """Invalida todos os caches relacionados a métricas"""
        self.metricas_cache.clear_all()
        self.graficos_cache.clear_all()
        self.kpis_cache.clear_all()
    
    def invalidate_on_data_change(self, model_name):
        """
        Invalida caches quando dados específicos mudam
        """
        invalidation_map = {
            'atleta': ['metricas_atletas', 'graficos_atletas', 'kpis_operacionais'],
            'competicao': ['metricas_competicoes', 'graficos_competicoes', 'kpis_qualidade'],
            'academia': ['metricas_academias', 'graficos_academias'],
        }
        
        if model_name.lower() in invalidation_map:
            for cache_key in invalidation_map[model_name.lower()]:
                self.metricas_cache.invalidate(cache_key)
                logger.info(f"Cache invalidado por mudança em {model_name}: {cache_key}")


# Instância global do gerenciador de cache
cache_manager = CacheManager()
    """Sistema de cache otimizado para estatísticas"""
    
    def __init__(self, timeout=300):  # 5 minutos por padrão
        self.timeout = timeout
    
    def get_key(self, nome, params=None):
        """Gera chave única para o cache"""
        base = f"stats_{nome}"
        if params:
            params_str = json.dumps(params, sort_keys=True)
            hash_params = hashlib.md5(params_str.encode()).hexdigest()
            return f"{base}_{hash_params}"
        return base
    
    def get_or_calculate(self, nome, calc_func, params=None, timeout=None):
        """Recupera dados do cache ou calcula se necessário"""
        key = self.get_key(nome, params)
        data = cache.get(key)
        
        if data is None:
            data = calc_func(params) if params else calc_func()
            cache_timeout = timeout or self.timeout
            cache.set(key, data, cache_timeout)
        
        return data
    
    def invalidate(self, nome, params=None):
        """Invalida uma entrada específica do cache"""
        key = self.get_key(nome, params)
        cache.delete(key)
    
    def invalidate_pattern(self, pattern):
        """Invalida todas as entradas que correspondem ao padrão"""
        # Nota: Esta função pode ser específica do backend de cache usado
        pass
    
    def get_stats(self):
        """Retorna estatísticas do próprio cache"""
        return {
            'timeout_default': self.timeout,
            'timestamp': timezone.now().isoformat()
        }


class CacheManager:
    """Gerenciador centralizado de cache para diferentes tipos de estatísticas"""
    
    def __init__(self):
        self.dashboard_cache = EstatisticasCache(timeout=300)     # 5 min
        self.graficos_cache = EstatisticasCache(timeout=600)      # 10 min  
        self.relatorios_cache = EstatisticasCache(timeout=1800)   # 30 min
        self.metricas_cache = EstatisticasCache(timeout=180)      # 3 min
    
    def get_cache_by_type(self, tipo):
        """Retorna o cache apropriado para o tipo de dados"""
        cache_mapping = {
            'dashboard': self.dashboard_cache,
            'graficos': self.graficos_cache,
            'relatorios': self.relatorios_cache,
            'metricas': self.metricas_cache,
        }
        return cache_mapping.get(tipo, self.dashboard_cache)
    
    def invalidate_all(self):
        """Invalida todos os caches"""
        cache.clear()
    
    def get_status(self):
        """Retorna status de todos os caches"""
        return {
            'dashboard': self.dashboard_cache.get_stats(),
            'graficos': self.graficos_cache.get_stats(),
            'relatorios': self.relatorios_cache.get_stats(),
            'metricas': self.metricas_cache.get_stats(),
        }


# Instância global do gerenciador de cache
cache_manager = CacheManager()

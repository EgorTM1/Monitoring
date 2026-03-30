from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client import REGISTRY
from fastapi import Request, Response
import time
from typing import Callable
import asyncio

# ========== МЕТРИКИ ==========

# Счётчик запросов (с метками: метод, эндпоинт, статус)
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

# Гистограмма времени выполнения запросов
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Счётчик активных запросов (Gauge)
ACTIVE_REQUESTS = Gauge(
    'http_active_requests',
    'Number of currently active HTTP requests'
)

# Счётчик ошибок
ERROR_COUNT = Counter(
    'http_errors_total',
    'Total number of HTTP errors',
    ['method', 'endpoint', 'error_type']
)


# ========== MIDDLEWARE ==========

class PrometheusMiddleware:
    """Middleware для сбора метрик Prometheus"""
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        # Увеличиваем счётчик активных запросов
        ACTIVE_REQUESTS.inc()
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Записываем метрики для успешного запроса
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            
            # Если ошибка клиента или сервера
            if response.status_code >= 400:
                ERROR_COUNT.labels(
                    method=request.method,
                    endpoint=request.url.path,
                    error_type=str(response.status_code)
                ).inc()
                
        except Exception as e:
            # Ошибка приложения
            ERROR_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                error_type=type(e).__name__
            ).inc()
            raise
            
        finally:
            duration = time.time() - start_time
            
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)
            
            ACTIVE_REQUESTS.dec()
        
        return response


# ========== ФУНКЦИЯ ДЛЯ ПОДКЛЮЧЕНИЯ ==========

def setup_metrics(app):
    """Подключение мониторинга к приложению"""
    
    # Добавляем middleware
    app.middleware("http")(PrometheusMiddleware())
    
    # Добавляем эндпоинт для метрик
    @app.get("/metrics", tags=['Metrics'])
    async def get_metrics():
        return Response(
            generate_latest(),
            media_type="text/plain"
        )
    
    # Эндпоинт для проверки здоровья
    @app.get("/health", tags=['Health'])
    async def health():
        return {"status": "healthy"}
    
    print("✅ Мониторинг настроен")
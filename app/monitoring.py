# app/monitoring.py
from prometheus_client import Counter, Histogram, Gauge

# Metrics
REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

LATENCY = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['endpoint']
)

MODEL_PREDICTIONS = Counter(
    'model_predictions_total',
    'Total number of predictions made'
)

ACTIVE_REQUESTS = Gauge(
    'api_active_requests',
    'Number of active requests'
)


def track_latency():
    def decorator(func):
        async def wrapper(*args, **kwargs):
            with LATENCY.labels(func.__name__).time():
                return await func(*args, **kwargs)

        return wrapper

    return decorator

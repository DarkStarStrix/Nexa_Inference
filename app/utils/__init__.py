# app/utils/__init__.py
from prometheus_client import Counter, Histogram
from fastapi import FastAPI

def setup_monitoring(app: FastAPI) -> None:
    """Setup monitoring metrics for the application"""
    global REQUEST_COUNT, REQUEST_LATENCY

    REQUEST_COUNT = Counter(
        'http_requests_total',
        'Total HTTP requests',
        ['method', 'endpoint', 'status']
    )

    REQUEST_LATENCY = Histogram(
        'http_request_duration_seconds',
        'HTTP request latency',
        ['method', 'endpoint']
    )

__all__ = ["setup_monitoring"]
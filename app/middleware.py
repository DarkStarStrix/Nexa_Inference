# app/middleware.py
from fastapi import Request
from app.monitoring import REQUEST_COUNT, ACTIVE_REQUESTS
import time
import logging

logger = logging.getLogger(__name__)

async def monitoring_middleware(request: Request, call_next):
    ACTIVE_REQUESTS.inc()
    start_time = time.time()

    try:
        response = await call_next(request)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise
    finally:
        ACTIVE_REQUESTS.dec()
        duration = time.time() - start_time
        logger.info(f"Request processed in {duration:.2f}s")
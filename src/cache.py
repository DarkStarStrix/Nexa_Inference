from redis import Redis
import redis
from typing import Any, Optional
import json
import pickle
from datetime import datetime, timedelta
import os

class RedisCache:
    def __init__(self):
        self.redis = Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=0,
            decode_responses=False  # Use bytes for binary data
        )
        self.model_cache_ttl = int(os.getenv('MODEL_CACHE_TTL', 3600))  # 1-hour default
        self.usage_cache_ttl = int(os.getenv('USAGE_CACHE_TTL', 86400))  # 24-hour default

    def get_model_cache(self, model_name: str, input_data: str) -> Optional[Any]:
        """Get cached model inference result."""
        cache_key = f"model:{model_name}:input:{hash(input_data)}"
        try:
            cached = self.redis.get(cache_key)
            if cached:
                return pickle.loads(cached)
        except (pickle.PickleError, redis.RedisError):
            pass
        return None

    def set_model_cache(self, model_name: str, input_data: str, result: Any) -> None:
        """Cache model inference result."""
        cache_key = f"model:{model_name}:input:{hash(input_data)}"
        try:
            self.redis.setex(
                cache_key,
                self.model_cache_ttl,
                pickle.dumps(result)
            )
        except (pickle.PickleError, redis.RedisError):
            pass

    def check_rate_limit(self, api_key: str, tier_limit: int) -> bool:
        """
        Check if request is within rate limits.
        tier_limit: int - maximum allowed requests for the tier.
        """
        current_month = datetime.now().strftime('%Y-%m')
        usage_key = f"usage:{api_key}:{current_month}"

        try:
            usage = self.redis.get(usage_key)
            current_usage = int(usage) if usage else 0

            if current_usage >= tier_limit:
                return False

            self.redis.incr(usage_key)
            if not usage:
                self.redis.expire(usage_key, self.usage_cache_ttl)
        except redis.RedisError:
            return False

        return True

    def track_usage(self, api_key: str, model_name: str, response_time: float) -> None:
        """Track API usage metrics."""
        timestamp = datetime.now().timestamp()
        usage_data = {
            'timestamp': timestamp,
            'model_name': model_name,
            'response_time': response_time
        }
        try:
            self.redis.zadd(f"metrics:{api_key}", {json.dumps(usage_data): timestamp})
            cutoff = (datetime.now() - timedelta(days=30)).timestamp()
            self.redis.zremrangebyscore(f"metrics:{api_key}", '-inf', cutoff)
        except (json.JSONDecodeError, redis.RedisError):
            pass

    def get_user_metrics(self, api_key: str) -> dict:
        """Get usage metrics for a user."""
        try:
            metrics = self.redis.zrange(f"metrics:{api_key}", 0, -1, withscores=True)
        except redis.RedisError:
            return {
                'total_calls': 0,
                'average_response_time': 0,
                'model_usage': {}
            }

        total_calls = len(metrics)
        avg_response_time = 0
        model_usage = {}

        for metric, _ in metrics:
            try:
                data = json.loads(metric.decode('utf-8'))
                avg_response_time += data['response_time']
                model_usage[data['model_name']] = model_usage.get(data['model_name'], 0) + 1
            except (json.JSONDecodeError, AttributeError):
                continue

        if total_calls > 0:
            avg_response_time /= total_calls

        return {
            'total_calls': total_calls,
            'average_response_time': avg_response_time,
            'model_usage': model_usage
        }

    def clear_expired_cache(self) -> None:
        """Clear expired cache entries."""
        try:
            for key in self.redis.scan_iter("model:*"):
                ttl = self.redis.ttl(key)
                if ttl == -2:  # Key does not exist
                    self.redis.delete(key)
        except redis.RedisError:
            pass

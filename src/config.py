import os
from supabase import create_client
import redis

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

TIER_LIMITS = {
    "free": 300,
    "premium-1k": 1000,
    "premium-5k": 5000,
    "premium-10k": 10000,
    "enterprise": float("inf")
}

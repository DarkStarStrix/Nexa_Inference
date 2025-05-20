from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from src.config import supabase, TIER_LIMITS

api_key_header = APIKeyHeader(name="X-API-Key")

def get_user_by_api_key(api_key: str):
    user = supabase.table("users").select("*").eq("api_key", api_key).execute()
    if not user.data:
        return None
    return user.data[0]

def increment_requests_used(api_key: str, current_count: int):
    supabase.table("users").update({"requests_used": current_count + 1}).eq("api_key", api_key).execute()

def get_tier_limit(tier: str):
    return TIER_LIMITS.get(tier, 300)

def verify_api_key(api_key: str = Security(api_key_header)):
    user_data = get_user_by_api_key(api_key)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid API key")
    tier = user_data["tier"]
    requests_used = user_data.get("requests_used", 0)
    limit = get_tier_limit(tier)
    if requests_used >= limit:
        raise HTTPException(status_code=429, detail="Usage limit exceeded")
    increment_requests_used(api_key, requests_used)
    return user_data

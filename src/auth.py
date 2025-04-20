from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from src.config import supabase, TIER_LIMITS

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    user = supabase.table("users").select("*").eq("api_key", api_key).execute()
    if not user.data:
        raise HTTPException(status_code=401, detail="Invalid API key")
    user_data = user.data[0]
    tier = user_data["tier"]
    requests_used = user_data.get("requests_used", 0)
    limit = TIER_LIMITS.get(tier, 300)
    if requests_used >= limit:
        raise HTTPException(status_code=429, detail="Usage limit exceeded")
    supabase.table("users").update({"requests_used": requests_used + 1}).eq("api_key", api_key).execute()
    return user_data

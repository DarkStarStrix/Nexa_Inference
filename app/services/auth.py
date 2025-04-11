# app/services/auth.py
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from supabase import create_client

from app.config import SUPABASE_URL, SUPABASE_KEY

api_key_header = APIKeyHeader(name="X-API-Key")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def verify_api_key(api_key: str = Security(api_key_header)):
    try:
        result = supabase.table("api_keys").select("*").eq("key", api_key)
        if not result.data:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")

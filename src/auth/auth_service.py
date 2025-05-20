import os
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from src.config import supabase, TIER_LIMITS

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_api_key() -> str:
    """Generate a secure API key."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def signup_user(email: str, password: str, tier: str = "free") -> dict:
    """
    Register a new user in Supabase.
    """
    # Create user in Supabase Auth
    auth_resp = supabase.auth.sign_up({"email": email, "password": password})
    if auth_resp.get("error"):
        raise HTTPException(status_code=400, detail=auth_resp["error"]["message"])
    user_id = auth_resp["user"]["id"]

    # Store user profile in 'users' table
    api_key = generate_api_key()
    profile_resp = supabase.table("users").insert({
        "id": user_id,
        "email": email,
        "tier": tier,
        "api_key": api_key,
        "requests_used": 0,
        "created_at": datetime().isoformat()
    }).execute()
    if profile_resp.get("error"):
        raise HTTPException(status_code=400, detail=profile_resp["error"]["message"])
    return {"id": user_id, "email": email, "api_key": api_key}

def authenticate_user(email: str, password: str) -> dict:
    """
    Authenticate user with Supabase Auth.
    """
    auth_resp = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if auth_resp.get("error"):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = auth_resp.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def get_user_by_api_key(api_key: str) -> Optional[dict]:
    """
    Retrieve user profile from Supabase by API key.
    """
    resp = supabase.table("users").select("*").eq("api_key", api_key).single().execute()
    if resp.get("error") or not resp.get("data"):
        return None
    return resp["data"]

def increment_requests_used(api_key: str, current_count: int):
    """
    Increment the requests_used field for a user.
    """
    supabase.table("users").update({"requests_used": current_count + 1}).eq("api_key", api_key).execute()

def get_tier_limit(tier: str) -> int:
    """
    Get the request limit for a user's tier.
    """
    return TIER_LIMITS.get(tier, 300)

def verify_api_key(api_key: str = Depends(oauth2_scheme)) -> dict:
    """
    Verify API key and enforce usage limits.
    """
    user = get_user_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    tier = user.get("tier", "free")
    requests_used = user.get("requests_used", 0)
    limit = get_tier_limit(tier)
    if requests_used >= limit:
        raise HTTPException(status_code=429, detail="Usage limit exceeded")
    increment_requests_used(api_key, requests_used)
    return user

# Example flow:
# 1. signup_user(email, password) -> creates user in Supabase and users table.
# 2. authenticate_user(email, password) -> authenticates and returns user info.
# 3. create_access_token({"sub": email}) -> returns JWT for session.
# 4. verify_api_key(api_key) -> checks API key and usage.

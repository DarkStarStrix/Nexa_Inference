from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4

class TierLevel(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class UsageLimits:
    LIMITS = {
        TierLevel.FREE: 300,
        TierLevel.PRO: 1000,
        TierLevel.ENTERPRISE: float('inf')
    }

    DATASET_PRICING = {
        500: 29.99,
        1000: 299.99,
        5000: 999.99,
        10000: 2499.99
    }

class User(BaseModel):
    id: UUID = uuid4()
    email: EmailStr
    password_hash: str
    tier: TierLevel = TierLevel.FREE
    api_keys: List[UUID] = []
    created_at: datetime = datetime.now()
    monthly_calls: int = 0
    workspace_id: Optional[UUID] = None
    budget_limit: Optional[float] = None

class APIKey(BaseModel):
    id: UUID = uuid4()
    user_id: UUID
    key: str
    name: str
    created_at: datetime = datetime.now()
    last_used: Optional[datetime] = None
    is_active: bool = True
    calls_count: int = 0

class Workspace(BaseModel):
    id: UUID = uuid4()
    name: str
    owner_id: UUID
    members: List[UUID] = []
    created_at: datetime = datetime.now()
    settings: dict = {}

class Usage(BaseModel):
    id: UUID = uuid4()
    user_id: UUID
    api_key_id: UUID
    model_name: str
    timestamp: datetime = datetime.now()
    response_time: float
    status: str
    request_size: int
    response_size: int

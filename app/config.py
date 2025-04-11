# config.py
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Supabase settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Stripe settings
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Stripe prices
STRIPE_PRICES = {
    "premium-1k": os.getenv("STRIPE_PREMIUM_1K_PRICE"),
    "premium-5k": os.getenv("STRIPE_PREMIUM_5K_PRICE"),
    "premium-10k": os.getenv("STRIPE_PREMIUM_10K_PRICE"),
    "enterprise": os.getenv("STRIPE_ENTERPRISE_PRICE")
}

# API rate limits
TIER_LIMITS = {
    "free": 300,
    "premium-1k": 1000,
    "premium-5k": 5000,
    "premium-10k": 10000,
    "enterprise": float('inf')
}

# Validate required environment variables
required_vars = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "STRIPE_SECRET_KEY",
    "STRIPE_WEBHOOK_SECRET"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")


def MODEL_CONFIG():
    return {
        "embedding_dim": 128,
        "hidden_dim": 256,
        "num_layers": 3,
        "weights_path": "weights.pth"
    }

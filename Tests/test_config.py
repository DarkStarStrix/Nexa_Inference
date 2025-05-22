# Test environment configuration
import os

# Test environment variables
os.environ['SUPABASE_URL'] = 'http://mock-supabase-url'
os.environ['SUPABASE_KEY'] = 'mock-supabase-key'
os.environ['REDIS_URL'] = 'redis://localhost:6379'
os.environ['MODEL_PATH'] = './models'
os.environ['LOG_LEVEL'] = 'DEBUG'

# Test configuration
TEST_CONFIG = {
    'API_VERSION': 'v1',
    'TIER_LIMITS': {
        'free': 100,
        'pro': 1000,
        'enterprise': 10000
    }
}

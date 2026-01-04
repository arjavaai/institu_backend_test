from supabase import create_client, Client
from .config import settings

def get_supabase_client() -> Client:
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_SERVICE_ROLE_KEY
    supabase: Client = create_client(url, key)
    return supabase

# Initialize a global client instance
supabase_admin = get_supabase_client()

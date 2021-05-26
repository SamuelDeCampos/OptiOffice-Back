from supabase_py import create_client, Client
from ..config import DB_CONFIG

url: str = DB_CONFIG.get('HOST_URL')
key: str = DB_CONFIG.get('HOST_KEY')

print('Url', url)
print('Key', key)

dbClient: Client = create_client(url, key)
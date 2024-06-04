import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ['SUPABASE_URL']
key: str = os.environ['SUPABASE_KEY']
supabase: Client = create_client(url, key)


response = supabase.table('goal_list').select("*").execute()
print("response", response)

# data, count = supabase.table('user').insert({"username": "test"}).execute()
# print("data", "data")
import configparser
from supabase import create_client, Client

settings = configparser.ConfigParser()
settings.read(['./main.config'])

url: str = settings['db_config']['SUPABASE_URL']
key: str = settings['db_config']['SUPABASE_KEY']

GLOBAL_CLIENT: Client = create_client(url, key)

def custom_client(*args, **kwargs) -> Client:
    """
    Proxy function to create a supabase client anywhere without having to import supabase.
    Uses config key and url if none are specified for either variable.
    """
    return create_client(url=url if 'url' not in kwargs else kwargs['url'], key=key if 'key' not in kwargs else kwargs['key'], *args, **kwargs)
import configparser
from supabase import create_client, Client

with configparser.ConfigParser() as settings:
    settings: configparser.ConfigParser
    settings.read(['../main.config'])

    
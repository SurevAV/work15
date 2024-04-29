import os
from dataclasses import dataclass
import uuid


openai_api_key = ""
bot_token = ""


db_name = 'ncdb'
db_user = 'postgres'
db_pwd = 'user'
db_host = 'localhost'
db_port = 5432



# 
@dataclass
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or openai_api_key
    BOT_TOKEN = os.getenv("BOT_TOKEN") or bot_token
    TOKENS_FOR_NEW_USER = 1
    DB_NAME = db_name
    DB_USER = db_user
    DB_PASSWORD = db_pwd
    DB_HOST = db_host
    DB_PORT = db_port
    PAYMENTS_PROVIDER_TOKEN = ''
    PERIOD_CONSULTANT = 30
    COST_CONSULTANT= 5000
    PERIOD_COMMENTATOR = 30
    COST_COMMENTATOR = 5000



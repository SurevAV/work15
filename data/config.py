import os
from dataclasses import dataclass
import uuid


openai_api_key = "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"
bot_token = "6039886909:AAE0OP7R_6XG2xZv2uTf3WO4bZjUG1wJgvo"


db_name = 'ncdb'
db_user = 'postgres'
db_pwd = 'user'
db_host = 'localhost'
db_port = 5432



# openai_api_key = "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"
# bot_token = "6056130831:AAFj5pAGtvImsSOsa9Ju5m3_Q4Lr3XyE_KQ"
#alembic init -t async migrations

#
# db_name = 'ncdb'
# db_user = 'user_10'
# db_pwd = '1234'
# db_host = 'localhost'
# db_port = 5432
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
    PAYMENTS_PROVIDER_TOKEN = '401643678:TEST:a6146ff1-02c9-40a0-aac7-f33bec7c7bbf'



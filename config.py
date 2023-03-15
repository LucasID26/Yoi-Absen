from pyrogram import Client 
import os

ID = os.environ['API_ID']
HASH = os.environ['API_HASH']
TOKEN = os.environ['BOT_TOKEN']


own = [1928677026]
bot = Client("Absen_Bot", 
             api_id=ID, 
             api_hash=HASH,
             bot_token=TOKEN,
             in_memory=True
            )
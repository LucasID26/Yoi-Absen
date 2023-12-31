from database import mydb 
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json

get_data = open("json/absen.json")
DB = json.load(get_data)

def wita():
  return


def wit():
  db.delete_many({"zona":"WIT"})


def wib():
  db.delete_many({"zona":"WIB"})


Wib = AsyncIOScheduler(timezone="Asia/Jakarta")
Wib.add_job(wib, trigger="cron",hour=0) 
Wib.start() 

Wit = AsyncIOScheduler(timezone="Asia/Jayapura")
Wit.add_job(wit, trigger="cron",hour=0) 
Wit.start() 

Wita = AsyncIOScheduler(timezone="Asia/Makassar")
Wita.add_job(wita, trigger="cron",hour=0) 
Wita.start()
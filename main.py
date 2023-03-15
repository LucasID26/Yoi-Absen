from config import bot 
import absen 
import schedule
from flask import Flask 
from threading import Thread
from pyrogram import idle


app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'


def run_flask():
  app.run(host='0.0.0.0', port=8080)
def thread():
  Thread(target=run_flask).start()
def run():
  thread()
  bot.start()
  idle() 
  bot.stop()
run()


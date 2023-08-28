from pyrogram import filters 
from pykeyboard import InlineKeyboard,InlineButton
from config import bot
from database import mydb
from pytz import timezone
from datetime import datetime 
from pykeyboard import InlineKeyboard,InlineButton
from decorator import bot_admin
import json

get_absen = open("json/absen.json")
DB = json.load(get_absen)



list_hari = {"Sunday":"Minggu",
             "Monday":"Senin",
             "Tuesday":"Selasa",
             "Wednesday":"Rabu",
             "Thursday":"Kamis",
             "Friday":"Jumat",
             "Saturday":"Sabtu"
            }
list_bulan = {"January":"Januari",
              "February":"Februari",
              "March":"Maret",
              "April":"April",
              "May":"Mei",
              "June":"Juni",
              "July":"Juli",
              "August":"Agustus",
              "September":"September",
              "October":"Oktober",
              "November":"November",
              "December":"Desember"
             }


 

 


@bot.on_message(filters.command("start")) 
async def start(client,m):
  if m.chat.type.value == "private":
    await m.reply_text("Masukan saya dalam group dan jadikan saya admin!")
  else:
    await m.reply_text("AYO MULAI ABSEN!")



@bot.on_message(filters.command(["start_wib","start_wita","start_wit"])) 
@bot_admin
async def absen(client,m):
  if m.chat.type.value == "private":
    return await m.reply_text("Perintah ini dibuat untuk digunakan di obrolan grup, bukan di pm!")
  chatid = str(m.chat.id)
  userid = str(m.from_user.id)
  if m.command[0] == "start_wib":
    wib = datetime.now(tz=timezone('Asia/Jakarta'))
    hari_wib = wib.strftime("%A")
    bulan_wib = wib.strftime("%B")
    tgl_wib = wib.strftime(f"Hari {list_hari[f'{hari_wib}']} , tanggal %d {list_bulan[f'{bulan_wib}']} %Y")
    if chatid in DB['WIB']:
      del DB['WIB'][chatid]
    if chatid in DB['WITA']:
      del DB['WITA'][chatid]
    if chatid in DB['WIT']:
      del DB['WIT'][chatid]
    button = InlineKeyboard()
    button.add(
    InlineButton("Hadir",callback_data='hadir_wib'))
    msg = await m.reply_text(f"__**START ABSEN**__: {m.chat.title}\n{tgl_wib} WIB\n\nTidak ada yang hadir!\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)
  
  elif m.command[0] == "start_wit":
    wit = datetime.now(tz=timezone('Asia/Jayapura'))
    hari_wit = wit.strftime("%A")
    bulan_wit = wit.strftime("%B")
    tgl_wit = wit.strftime(f"Hari {list_hari[f'{hari_wit}']} , tanggal %d {list_bulan[f'{bulan_wit}']} %Y")
    if chatid in DB['WIB']:
      del DB['WIB'][chatid]
    if chatid in DB['WITA']:
      del DB['WITA'][chatid]
    if chatid in DB['WIT']:
      del DB['WIT'][chatid]
    button = InlineKeyboard()
    button.add(
    InlineButton("Hadir",callback_data='hadir_wit'))
    msg = await m.reply_text(f"__**START ABSEN**__: {m.chat.title}\n{tgl_wit} WIT\n\nTidak ada yang hadir!\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)

  elif m.command[0] == "start_wita":
    wita = datetime.now(tz=timezone('Asia/Makassar'))
    hari_wita = wita.strftime("%A")
    bulan_wita = wita.strftime("%B")
    tgl_wita = wita.strftime(f"Hari {list_hari[f'{hari_wita}']} , tanggal %d {list_bulan[f'{bulan_wita}']} %Y")
    if chatid in DB['WIB']:
      del DB['WIB'][chatid]
    if chatid in DB['WITA']:
      del DB['WITA'][chatid]
    if chatid in DB['WIT']:
      del DB['WIT'][chatid]
    button = InlineKeyboard()
    button.add(
    InlineButton("Hadir",callback_data='hadir_wita'))
    msg = await m.reply_text(f"__**START ABSEN**__: {m.chat.title}\n{tgl_wita} WITA\n\nTidak ada yang hadir!\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)
  with open("json/absen.json") as data:
    json.dump(DB,data,indent=2)
  await msg.pin()   

    
#CALLBACK      
@bot.on_callback_query(filters.regex("^hadir_wib$"))
async def callback(_,call):
  global DB
  wib = datetime.now(tz=timezone('Asia/Jakarta'))
  time_wib = wib.strftime("%H:%M:%S")
  hari_wib = wib.strftime("%A")
  bulan_wib = wib.strftime("%B")
  tgl_wib = wib.strftime(f"Hari {list_hari[f'{hari_wib}']} , tanggal %d {list_bulan[f'{bulan_wib}']} %Y")
  user = str(call.from_user.id)
  chatid = str(call.message.chat.id)
  button = InlineKeyboard()
  button.add(
    InlineButton("Hadir",callback_data='hadir_wib'))
  hasil = ""
  if chatid in DB['WIB']:
    if user in DB['WIB'][chatid]:
      await call.answer("Kamu sudah hadir hari ini!",True)
    else:
      DB['WIB'][chatid] = {user: time_wib)
      with open("json/absen.json") as data:
        json.dump(DB,data,indent=2)
      angka = 1
      for users in DB['WIB'][chatid]:
        nama = (await bot.get_users(int(users))).first_name
        waktu = DB['WIB'][chatid][users]
        hasil += f"{angka}.{nama} → {waktu}\n" 
        angka += 1
      return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wib} WIB\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)

  else:
    DB['WIB'] = {chatid: {user: time_wib}}
    with open("json/absen.json") as data:
      json.dump(DB,data,indent=2)
    angka = 1
    for users in DB['WIB'][chatid]:
      nama = (await bot.get_users(int(users))).first_name
      waktu = DB['WIB'][chatid][users]
      hasil += f"{angka}.{nama} → {waktu}\n"
      angka += 1
    return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wib} WIB\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)
      

@bot.on_callback_query(filters.regex("^hadir_wita$"))
async def callback(_,call):
  global DB
  wita = datetime.now(tz=timezone('Asia/Makassar'))
  time_wita = wita.strftime("%H:%M:%S") 
  hari_wita = wita.strftime("%A")
  bulan_wita = wita.strftime("%B")
  tgl_wita = wita.strftime(f"Hari {list_hari[f'{hari_wita}']} , tanggal %d {list_bulan[f'{bulan_wita}']} %Y")
  user = str(call.from_user.id)
  chatid = str(call.message.chat.id)
  button = InlineKeyboard()
  button.add(
    InlineButton("Hadir",callback_data='hadir_wita')

  hasil = ""
  if chatid in DB['WITA']:
    if user in DB['WITA'][chatid]:
      await call.answer("Kamu sudah hadir hari ini!",True)
    else:
      DB['WITA'][chatid] = {user: time_wita}}
      with open("json/absen.json") as data:
        json.dump(DB,data,indent=2)
      angka = 1
      for users in DB['WITA'][chatid]:
        nama = (await bot.get_users(int(users))).first_name
        waktu = DB['WITA'][chatid][users]
        hasil += f"{angka}.{nama} → {waktu}\n"
        angka += 1
      return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wita} WITA\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)

  else:
    DB['WITA'] = {chatid: {user: time_wita}}
    with open("json/absen.json") as data:
      json.dump(DB,data,indent=2)
    angka = 1
    for users in DB['WITA'][chatid]:
      nama = (await bot.get_users(int(users))).first_name
      waktu = DB['WITA'][chatid][users]
      hasil += f"{angka}.{nama} → {waktu}\n"
      angka += 1
    return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wita} WITA\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)  

  
@bot.on_callback_query(filters.regex("^hadir_wit$"))
async def callback(_,call):
  global DB
  wit = datetime.now(tz=timezone('Asia/Jayapura'))
  time_wit = wit.strftime("%H:%M:%S") 
  hari_wit = wit.strftime("%A")
  bulan_wit = wit.strftime("%B")
  tgl_wit = wit.strftime(f"Hari {list_hari[f'{hari_wit}']} , tanggal %d {list_bulan[f'{bulan_wit}']} %Y")
  user = str(call.from_user.id)
  chatid = str(call.message.chat.id)
  button = InlineKeyboard()
  button.add(
    InlineButton("Hadir",callback_data='hadir_wit'))
  hasil = ""
  if chatid in DB['WIT']:
    if user in DB['WIT'][chatid]:
      await call.answer("Kamu sudah hadir hari ini!",True)
    else:
      DB['WIT'][chatid] = {user: time_wit}}
      with open("json/absen.json") as data:
        json.dump(DB,data,indent=2)
      angka = 1
      for users in DB['WIT'][chatid]:
        nama = (await bot.get_users(int(users))).first_name
        waktu = DB['WIT'][chatid][users]
        hasil += f"{angka}.{nama} → {waktu}\n"
        angka += 1
      return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wit} WIT\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)

  else:
    DB['WIT'] = {chatid: {user: time_wit}}
    with open("json/absen.json") as data:
      json.dump(DB,data,indent=2)
    angka = 1
    for users in DB['WIT'][chatid]:
      nama = (await bot.get_users(int(users))).first_name
      waktu = DB['WIT'][chatid][users]
      hasil += f"{angka}.{nama} → {waktu}\n"
      angka += 1
    return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wit} WIT\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)  


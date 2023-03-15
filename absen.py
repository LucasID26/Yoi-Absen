from pyrogram import filters 
from pykeyboard import InlineKeyboard,InlineButton
from config import bot
from database import mydb
from pytz import timezone
from datetime import datetime 
from pykeyboard import InlineKeyboard,InlineButton
from decorator import bot_admin


db = mydb["Absen_Bot"] 



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
  chatid = m.chat.id
  userid = str(m.from_user.id)
  key = {"chatid": chatid}
  if m.command[0] == "start_wib":
    wib = datetime.now(tz=timezone('Asia/Jakarta'))
    hari_wib = wib.strftime("%A")
    bulan_wib = wib.strftime("%B")
    tgl_wib = wib.strftime(f"Hari {list_hari[f'{hari_wib}']} , tanggal %d {list_bulan[f'{bulan_wib}']} %Y")
    if db.find_one(key):
      db.delete_many(key)
    button = InlineKeyboard()
    button.add(
    InlineButton("Hadir",callback_data='hadir_wib'))
    msg = await m.reply_text(f"__**START ABSEN**__: {m.chat.title}\n{tgl_wib} WIB\n\nTidak ada yang hadir!\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)
  
  elif m.command[0] == "start_wit":
    wit = datetime.now(tz=timezone('Asia/Jayapura'))
    hari_wit = wit.strftime("%A")
    bulan_wit = wit.strftime("%B")
    tgl_wit = wit.strftime(f"Hari {list_hari[f'{hari_wit}']} , tanggal %d {list_bulan[f'{bulan_wit}']} %Y")
    if db.find_one(key):
      db.delete_many(key)
    button = InlineKeyboard()
    button.add(
    InlineButton("Hadir",callback_data='hadir_wit'))
    msg = await m.reply_text(f"__**START ABSEN**__: {m.chat.title}\n{tgl_wit} WIT\n\nTidak ada yang hadir!\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)
  
  elif m.command[0] == "start_wita":
    wita = datetime.now(tz=timezone('Asia/Makassar'))
    hari_wita = wita.strftime("%A")
    bulan_wita = wita.strftime("%B")
    tgl_wita = wita.strftime(f"Hari {list_hari[f'{hari_wita}']} , tanggal %d {list_bulan[f'{bulan_wita}']} %Y")
    if db.find_one(key):
      db.delete_many(key)
    button = InlineKeyboard()
    button.add(
    InlineButton("Hadir",callback_data='hadir_wita'))
    msg = await m.reply_text(f"__**START ABSEN**__: {m.chat.title}\n{tgl_wita} WITA\n\nTidak ada yang hadir!\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)
  await msg.pin()   

    
#CALLBACK      
@bot.on_callback_query(filters.regex("^hadir_wib$"))
async def callback(_,call):
  wib = datetime.now(tz=timezone('Asia/Jakarta'))
  time_wib = wib.strftime("%H:%M:%S")
  hari_wib = wib.strftime("%A")
  bulan_wib = wib.strftime("%B")
  tgl_wib = wib.strftime(f"Hari {list_hari[f'{hari_wib}']} , tanggal %d {list_bulan[f'{bulan_wib}']} %Y")
  user = call.from_user.id
  chatid = call.message.chat.id
  button = InlineKeyboard()
  button.add(
    InlineButton("Hadir",callback_data='hadir_wib'))
  key = {"chatid": chatid}
  key1 = {"chatid": chatid,"userid": user} 
  hasil = ""
  if db.find_one(key):
    if db.find_one(key1):
      await call.answer("Kamu sudah hadir hari ini!",True)
    else:
      db.insert_one({"chatid": chatid,"userid": user,"time": time_wib,"zona": "WIB","msgid":call.message.id})
      angka = 1
      for users in db.find(key):
        nama = (await bot.get_users(users["userid"])).first_name
        waktu = users["time"] 
        hasil += f"{angka}.{nama} → {waktu}\n" 
        angka += 1
      return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wib} WIB\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)

  else:
    db.insert_one({"chatid": chatid,"userid": user,"time": time_wib,"zona": "WIB","msgid":call.message.id})
    angka = 1
    for users in db.find(key):
      nama = (await bot.get_users(users["userid"])).first_name
      waktu = users["time"] 
      hasil += f"{angka}.{nama} → {waktu}\n"
      angka += 1
    return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wib} WIB\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)
      

@bot.on_callback_query(filters.regex("^hadir_wita$"))
async def callback(_,call): 
  wita = datetime.now(tz=timezone('Asia/Makassar'))
  time_wita = wita.strftime("%H:%M:%S") 
  hari_wita = wita.strftime("%A")
  bulan_wita = wita.strftime("%B")
  tgl_wita = wita.strftime(f"Hari {list_hari[f'{hari_wita}']} , tanggal %d {list_bulan[f'{bulan_wita}']} %Y")
  user = call.from_user.id
  chatid = call.message.chat.id
  button = InlineKeyboard()
  button.add(
    InlineButton("Hadir",callback_data='hadir_wita'))
  key = {"chatid": chatid}
  key1 = {"chatid": chatid,"userid": user} 
  hasil = ""
  if db.find_one(key):
    if db.find_one(key1):
      await call.answer("Kamu sudah hadir hari ini!",True)
    else:
      db.insert_one({"chatid": chatid,"userid": user,"time": time_wita,"zona": "WITA","msgid":call.message.id}) 
      angka = 1
      for users in db.find(key):
        nama = (await bot.get_users(users["userid"])).first_name
        waktu = users["time"] 
        hasil += f"{angka}.{nama} → {waktu}\n"
        angka += 1
      return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wita} WITA\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)

  else:
    db.insert_one({"chatid": chatid,"userid": user,"time": time_wita,"zona": "WITA","msgid":call.message.id})
    angka = 1
    for users in db.find(key):
      nama = (await bot.get_users(users["userid"])).first_name
      waktu = users["time"] 
      hasil += f"{angka}.{nama} → {waktu}\n"
      angka += 1
    return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wita} WITA\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)  

  
@bot.on_callback_query(filters.regex("^hadir_wit$"))
async def callback(_,call):
  wit = datetime.now(tz=timezone('Asia/Jayapura'))
  time_wit = wit.strftime("%H:%M:%S") 
  hari_wit = wit.strftime("%A")
  bulan_wit = wit.strftime("%B")
  tgl_wit = wit.strftime(f"Hari {list_hari[f'{hari_wit}']} , tanggal %d {list_bulan[f'{bulan_wit}']} %Y")
  user = call.from_user.id
  chatid = call.message.chat.id
  button = InlineKeyboard()
  button.add(
    InlineButton("Hadir",callback_data='hadir_wit'))
  key = {"chatid": chatid}
  key1 = {"chatid": chatid,"userid": user} 
  hasil = ""
  if db.find_one(key):
    if db.find_one(key1):
      await call.answer("Kamu sudah hadir hari ini!",True)
    else:
      db.insert_one({"chatid": chatid,"userid": user,"time": time_wit,"zona": "WIT","msgid":call.message.id})
      angka = 1
      for users in db.find(key):
        nama = (await bot.get_users(users["userid"])).first_name
        waktu = users["time"] 
        hasil += f"{angka}.{nama} → {waktu}\n"
        angka += 1
      return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wit} WIT\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)

  else:
    db.insert_one({"chatid": chatid,"userid": user,"time": time_wit,"zona": "WIT","msgid":call.message.id}) 
    angka = 1
    for users in db.find(key):
      nama = (await bot.get_users(users["userid"])).first_name
      waktu = users["time"] 
      hasil += f"{angka}.{nama} → {waktu}\n"
      angka += 1
    return await call.message.edit_text(f"__**START ABSEN**__: {call.message.chat.title}\n{tgl_wit} WIT\n\n{hasil}\n\nSilahkan klik button dibawah untuk absen!",reply_markup=button)  


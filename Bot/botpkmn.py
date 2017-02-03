# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6
import sys
import re
import telebot
from telebot import types
import time 
import json
import urllib
import random

import sqlite3
con = sqlite3.connect('pkmnbot.db',check_same_thread = False)
c = con.cursor()
pkmn = ""

TOKEN = '' 
INSULTS = ["eres gilipollas", "cómeme los huevos", "abrazafarolas","bocachancla", "parguela","eres tan feo que ni tu madre estaba en el parto", "me voy a cagar en las cuatro farolas que alumbran la tumba de tu puta madre", "dile a tu madre que deje de cambiarse de pintalabios que me está dejando la polla como un arcoiris", "eres tan feo que cuando te miras al espejo te pegas en defensa propia", "tu madre es tan puta que se quitó un ojo para tener un agujero más.", "eres tan gordo que tu grupo sanguíneo es A-peritivo", "eres homoretrasado","sabes menos de pokémon que Fola", "eres más inútil que Hydreigon firme", "eres tan tonto que te han cogido de tronista"]


usuarios = [line.rstrip('\n') for line in open('users.txt')] 

bot = telebot.TeleBot(TOKEN) 


grupos_admitidos = [-1001087339246, -1001031662216, -1001059767714,-1001073576848] #Aquí se tendrán que añadir a mano los ID de los grupos que usen el bot (grupo, liga, asd)
admins = [1896312, 9662836]

def listener(messages):
	for m in messages:
		cid = m.chat.id
		uid = m.from_user.id
		uname = m.from_user.username
			
	#if m.content_type == 'text':
		if m.text:


##########################################################
#################### Encuesta Bienvenida #################
			@bot.message_handler(func=lambda m: True, content_types=['new_chat_member'])
			def on_user_joins(m):
				cid = m.chat.id
				cname = m.chat.title
				bienvenida = ""
				if(m.new_chat_member.username=="PKMNFCbot"):
					l= 1
				
				else:
					if (m.new_chat_member.username is None):
						nun = ""
						nun = m.new_chat_member.first_name
						if (m.new_chat_member.last_name is not None):
							nun += " "
							nun += m.new_chat_member.last_name
							bienvenida = "Bienvenido al grupo "
							bienvenida += str(cname)
							bienvenida += " "
						else: 
							bienvenida = "Bienvenido al grupo "
							bienvenida += str(cname)
							bienvenida += " "
					else:
						nun = m.new_chat_member.username
						bienvenida = "Bienvenido al grupo "
						bienvenida += str(cname)
						bienvenida += " @"
					#	bienvenida += "<b>Pokémon</b> @"
					bot.send_message(cid, str(bienvenida) + str(nun) +
					", vamos a proceder a hacerte la encuesta de entrada:\n 1.- ¿Nostalfag?\n 2.- ¿Charmander, Squirtle o Bulbasaur?\n 3.-¿Legalfag o Piratafag?\n 4.-¿Fola sí o Fola no?\n<a href='https://raw.githubusercontent.com/Intervencion/PKMNFCbot/master/Audios/pokemon.mp3'> </a>\nSi te interesa saber las funciones que tiene RotomDex, ábreme chat en PRIVADO y hazme /help", parse_mode = "HTML")
			mensaje = "User: " + str(m.from_user.first_name) + "\n"
			if cid < 0:
				mensaje += "Chat: " + str(m.chat.title) + "\n"
				mensaje += "UserID: [" + str(uid) + "]"
			if cid < 0:
				mensaje += " ChatID: [" + str(cid) + "]"
				mensaje += "\n"
				mensaje += "Mensaje: " + m.text + "\n"
				mensaje += "-------------------------------\n"
			else:
				mensaje += "UserID: [" + str(uid) + "]\n"
				mensaje += "Mensaje: " + m.text + "\n"
				mensaje += "-------------------------------\n"
				
			if(m.text.startswith("!") or m.text.startswith("/")):
				f = open('log.txt', 'a')
				f.write(mensaje)
				f.close()
				patata = open('id.txt', 'a')
				patata.write("@" + str(uname) + "[" + str(uid) + "]" + "\n")
				patata.close()
				print (mensaje)

bot.set_update_listener(listener)





























#############################################
###############FUNCIONES#####################




@bot.message_handler(commands=['addfc']) 
def command_addfc(m):
	cid = m.chat.id
	uid = m.from_user.id
	if (m.from_user.username is None):
		uname = m.from_user.first_name + " " + m.from_user.last_name
	else:
		uname = m.from_user.username
	if ((cid in grupos_admitidos) or (cid in admins)):
		try:
			fc = m.text.split(' ', 1)[1].replace(" ","")
			fc.capitalize()
			pattern = '^\d\d\d\d-\d\d\d\d-\d\d\d\d$'
			if re.match(pattern, fc, flags=0):
				try:
				  c.execute("INSERT INTO PKMN (IDUSER,ALIAS,FC) VALUES ('"+ str(uid) + "', '@"+ uname.capitalize() + "','" + fc + "')")
				  bot.send_message( cid, "Se ha registrado a *" + uname + "* con Friend Code " + "*" + fc + "*" + ".", parse_mode = "Markdown")
				  con.commit()
	
				except sqlite3.Error:
				  bot.send_message( cid, "Ya has introducido tu código a la DB, si quieres editarlo usa /editFC")
			else:
				bot.send_message(cid, "El formato del comando es /addfc *XXXX-XXXX-XXXX* donde X son números.", parse_mode = "Markdown")
		  
		except:
			bot.send_message( cid, "El formato del comando es /addfc *XXXX-XXXX-XXXX* donde X son números.", parse_mode = "Markdown")
	else:
		bot.send_message( cid, "Este bot solo funciona en grupos designados. Para entrar en la lista blanca usa /contact desde el grupo en el que quieras usar el bot y evaluaremos el caso.")
		print (str(uname), m.text)





@bot.message_handler(commands=['fc'])
def command_fc(m):
	cid = m.chat.id 
	uname = m.from_user.username
	uid = m.from_user.id
	if ((cid in grupos_admitidos) or (cid in admins)):
		arrayl = []
		try:
		
			c.execute("SELECT iduser,alias,fc from PKMN ORDER BY alias ASC")
		
		
			for i in c:
				alias_resultado = i[1] + ": "
				fc_resultado = i[2]
				p = alias_resultado + fc_resultado
				arrayl.append(p)
			
			f = str(arrayl).replace("'","")
			print(arrayl)
			bot.send_message( cid, " *" + f.replace(",", "\n").replace("[","").replace("]","") + "*", parse_mode = "Markdown")
			con.commit()
		except sqlite3.Error:
			bot.send_message( cid, "No hemos podido mostrarte la lista")
	else:
		bot.send_message( cid, "Este bot solo funciona en grupos designados. Para entrar en la lista blanca usa /contact desde el grupo en el que quieras usar el bot y evaluaremos el caso.")		
		






@bot.message_handler(commands=['editfc']) 
def command_editfc(m):
	cid = m.chat.id
	uid = m.from_user.id
	nu = m.from_user.username
	if (m.from_user.username is None):
		uname = m.from_user.first_name + " " + m.from_user.last_name
	else:
		uname = m.from_user.username
	if ((cid in grupos_admitidos) or (cid in admins)):
		try:
			fc = m.text.split(' ', 1)[1].replace(" ","")
			pattern = '^\d\d\d\d-\d\d\d\d-\d\d\d\d$'
			if re.match(pattern, fc, flags=0):
				try:
				  c.execute("UPDATE PKMN SET 'fc' = '" + fc + "', 'alias'='@"+ nu + "' WHERE iduser = " + str(uid))
				  bot.send_message( cid, "Se ha cambiado el registro de *" + nu + "* ahora con *Friend Code* *" + fc + "*.", parse_mode = "Markdown")
				  con.commit()
	
				except sqlite3.Error:
				  bot.send_message( cid, "Ha ocurrido un error. Inténtalo de nuevo.")
			else:
				
				bot.send_message(cid, "El formato del comando es /editfc *XXXX-XXXX-XXXX* donde X son números.", parse_mode = "Markdown")
		  
		except:
			bot.send_message( cid, "El formato del comando es /editfc *XXXX-XXXX-XXXX* donde X son números.", parse_mode = "Markdown")
	else:
		bot.send_message( cid, "Este bot solo funciona en grupos designados. Para entrar en la lista blanca usa /contact desde el grupo en el que quieras usar el bot y evaluaremos el caso.")






@bot.message_handler(commands=['mifc']) 
def command_mifc(m):
	cid = m.chat.id
	uid = m.from_user.id
	if (m.from_user.username is None):
		uname = m.from_user.first_name + " " + m.from_user.last_name
	else:
		uname = m.from_user.username
	if ((cid in grupos_admitidos) or (cid in admins)):
		
		try:
			c.execute("SELECT alias,fc from PKMN WHERE iduser=" + str(uid))
			
			for i in c:
				alias_resultado = i[0] + " "
				fc_resultado = i[1]
				
			bot.send_message( cid, "*" + alias_resultado + "*: " + fc_resultado, parse_mode = "Markdown")
			con.commit()
		except:
			bot.send_message( cid, "Tu fc no aparece en la lista", parse_mode = "Markdown")
	else:
		bot.send_message( cid, "Este bot solo funciona en grupos designados. Para entrar en la lista blanca usa /contact desde el grupo en el que quieras usar el bot y evaluaremos el caso.")

	







@bot.message_handler(commands=['tetas'])
def command_boobs(message):
  response = urllib.request.urlopen('http://api.oboobs.ru/noise/1')
  i = 0
  while i < 10:
    data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    if len(data) < 1:
      i += 1
      response = urllib.request.urlopen('http://api.oboobs.ru/noise/1')
      continue
    else:
      bot.send_message(message.chat.id, 'http://media.oboobs.ru/' + data[0]['preview'])
      return
  bot.send_message(message.chat.id, '¿Qué es una teta?')
  
  




@bot.message_handler(commands=['culos'])
def command_butts(message):
  response = urllib.request.urlopen('http://api.obutts.ru/noise/1')
  i = 0
  while i < 10:
    data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    if len(data) < 1:
      i += 1
      response = urllib.request.urlopen('http://api.obutts.ru/noise/1')
      continue
    else:
      bot.send_message(message.chat.id, 'http://media.obutts.ru/' + data[0]['preview'])
      return
  bot.send_message(message.chat.id, '¿Qué es un culo?')
  










###############################################################
#######################COMANDOS DE LINKS#######################








@bot.message_handler(commands=['plati'])
def command_plati(m):
	bot.reply_to(m,'<a href="http://www.forocoches.com/foro/showthread.php?p=248515995#post248515995">Plataforma Pokémon Forocoches</a>', parse_mode="HTML", disable_web_page_preview=True)






@bot.message_handler(commands=['liga'])
def command_liga(m):
	bot.reply_to(m,'<a href="http://www.forocoches.com/foro/showthread.php?t=5293279">Liga Forocoches (Ed. Alola)</a>', parse_mode="HTML", disable_web_page_preview=True)	
	
	




@bot.message_handler(commands=['info'])
def command_info(m):
	cid = m.chat.id
	try:
		dex = m.text.split(' ', 1)[1].replace(" ","_")
		bot.reply_to(m,'http://es.pokemon.wikia.com/wiki/' + str(dex), disable_web_page_preview=True)	
	except:
		bot.send_message(cid, "El formato del comando es /info *X* donde X es el nombre del pokémon, movimiento u objeto.", parse_mode = "Markdown")
	






@bot.message_handler(commands=['festiplaza'])
def command_fiestiplaza(m):
	bot.reply_to(m,'<a href="https://docs.google.com/document/d/1tBMEb8xfogGqUqbxHuWC6LupSe7-3bKbCpGVF8nSVRA/edit">Toda la información sobre la Festiplaza.</a>', parse_mode="HTML", disable_web_page_preview=True)
	





@bot.message_handler(commands=['resort'])
def command_resort(m):
	bot.reply_to(m,'<a href="https://docs.google.com/document/d/1ANGMKXv9zQBh1iYYGxthpp5kGueDpbBYCseR-bsJc60/edit">Toda la información sobre el Resort.</a>', parse_mode="HTML", disable_web_page_preview=True)
	
	
	
	


@bot.message_handler(commands=['evs'])
def command_evs(m):
	bot.reply_to(m,"""*HP*\n*–* `Caterpie` : Ruta 1. 1 EV de HP\n*–* `Makuhita` : Ruta 2. 1 EV de HP
	\n\n*Ataque*\n*–* `Pikipek` : Ruta 1. 1 EV de Ataque\n*–* `Yangoos` : Ruta 1, Ruta 2 (Por el día). 1 EV de Ataque
	\n*–* `Mankey` : Ruta 3. 1 EV de Ataque\n\n*Defensa*\n*–* `Roggenrola` : Colina Dequilate. 1 EV de Defensa
	\n*–* `Cubone` : Área Volcánica Wela. 1 EV de Defensa\n*–* `Geodude` : Ruta 12. 1 EV de Defensa
	\n*–* `Torkoal` : Ruta 12. 2 EVs de Defensa\n\n*Ataque Especial*\n*–* `Magnemite` : Escuela de Entrenadores (Ruta 1). 
	1 EV de Ataque Especial\n*–* `Oricorio` : Jardines de Melemele. 2 EVs de Ataque Especial\n\n*Defensa Especial*
	\n*–* `Tentacool` : Mar de Melemele (Surf). 1 EV de Defensa Especial\n*–* `Drowzee` : Ruta 2. 1 EV de Defensa Especial
	\n\n*Velocidad*\n*–* `Wingull` : Ruta 1, Afueras de Akala. 1 EV de Velocidad\n*–* `Rattata de Alola` : Ruta 1, Ruta 2 (Por la noche). 
	1 EV de Velocidad\n*–* `Meowth de Alola` : Escuela de Entrenadores (Ruta 1), Ruta 2. 1 EV de Velocidad\n*–* `Spearow` : Ruta 2, Ruta 3. 
	1 EV de Velocidad""", parse_mode="markdown", disable_web_page_preview=True)






@bot.message_handler(commands=['natus'])
def command_natu(m):
	bot.reply_to(m,"*Naturalezas*[ ](http://i.imgur.com/IRFr5SG.jpg)", parse_mode="Markdown")
	
	



@bot.message_handler(commands=['btn'])
def command_evs0(m):
	cid = m.chat.id
	markup = types.InlineKeyboardMarkup()
	bttn = types.InlineKeyboardButton("Botón de prueba" , url="https://telegram.me/PKMNFCbot?start=evs")
#	b1 = types.InlineKeyboardButton("Botón de prueba" , url="/evs")
	markup.add(bttn)
	bot.reply_to(m,"Mensaje para botón de prueba", reply_markup=markup)
	
	
	




################################################################
################################################################
################################################################
########################COMANDOS STANDAR########################





@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	if m.text.find(" ") != -1:
		comando = m.text.split(' ', 1)[1] #// Deeplinking
	else:
		if not str(cid) in usuarios:
			usuarios.append(str(cid))
#			aux = open( '/home/axel/bots/users.txt', 'a') # Y lo insertamos en el fichero 'users.txt'
			aux = open( 'users.txt', 'a')
			aux.write( "id:"+ str(cid) + " user: " + str(m.chat.username) + "\n")
			aux.close()
			bot.send_message( cid, "Bienvenido al bot \n Si encuentras algún bug o dato erróneo, no dudes hacérnoslo saber con /bug y la descripción del mismo.")
		else:
			bot.send_message( cid, "Bienvenido al bot \n Si encuentras algún bug o dato erróneo, no dudes hacérnoslo saber con /bug y la descripción del mismo.")

	#if comando == 'evs':
	#	command_evs(m)
		
		
		




@bot.message_handler(commands=['help'])
def command_help(m):
	cid = m.chat.id
	bot.send_message(cid, """Los comandos de este bot son los siguientes:\n/addfc XXXX-XXXX-XXXX  
	---- Añadir tu Friend Code a la lista. \n/editfc XXXX-XXXX-XXXX  ---- Editar tu Friend Code y tu alias guardados. "
	\n/fc ---- Te permite ver la lista de Friend Code del grupo. \n/mifc ---- Te permite ver tu *Friend Code*. "
	\n/stats P ---- Dónde P es un pokémon, devuelve los stats y sus habilidades. \n/evs ---- Muestra una lista para farmear evs. "
	\n/festiplaza ----- Devuelve el link con toda la info de la festiplaza."
	\n/plati ----- Devuelve el link de la plataforma pokémon de forocoches. \n/liga ----- Devuelve el link de la liga pokémon de forocoches. "
	\n/info X ---- Devuelve el link de wikidex con lo introducido.\n/bug --- Reporta un bug a los desarrolladores.\n/contact --- Manda un mensaje a los desarrolladores.""")
	
	





@bot.message_handler(commands=['contact'])
def command_contact(m):
	cid = m.chat.id
	uid = m.from_user.id
	uname = m.from_user.username
	try:
		texto = m.text.split(' ', 1)[1]
		mensaje = "User: " + str(m.from_user.first_name) + "\n"
		mensaje += "Chat: " + str(m.chat.title) + "\n"
		mensaje += "UserID: [" + str(uid) + "]"
		mensaje += " ChatID: [" + str(cid) + "]"
		mensaje += "\n"
		mensaje += "Mensaje: " + str(texto) + "\n"
		mensaje += "-------------------------------\n"

		f = open('contacto.txt', 'a')
		f.write(mensaje)
		f.close()
		print ("Mensaje guardado en contacto.txt")
		bot.reply_to(m,"Tu mensaje ha sido recibido.")	
		bot.send_message(admins[0], "Hay un mensaje nuevo de @" + str(uname) + " [" + str(uid) + "] enviado desde <i>" + str(m.chat.title) + "</i> [" + str(cid) + "] en <code>contacto.txt</code>.", parse_mode = "HTML")
	except:
		bot.send_message(cid, "El formato del comando es /contact *X* donde X es el mensaje que quieras enviar.", parse_mode = "Markdown")




@bot.message_handler(commands=['bug'])
def command_bug(m):
	cid = m.chat.id
	uid = m.from_user.id
	uname = m.from_user.username
	try:
		texto = m.text.split(' ', 1)[1]
		mensaje = "User: " + str(m.from_user.first_name) + "\n"
		mensaje += "Chat: " + str(m.chat.title) + "\n"
		mensaje += "UserID: [" + str(uid) + "]"
		mensaje += " ChatID: [" + str(cid) + "]"
		mensaje += "\n"
		mensaje += "Mensaje: " + str(texto) + "\n"
		mensaje += "-------------------------------\n"

		f = open('bugs.txt', 'a')
		f.write(mensaje)
		f.close()
		print ("Mensaje guardado en bugs.txt")
		bot.reply_to(m,"Tu mensaje ha sido recibido.")	
		bot.send_message(admins[0], "Hay un mensaje nuevo de @" + str(uname) + " [" + str(uid) + "] enviado desde <i>" + str(m.chat.title) + "</i> [" + str(cid) + "] en <code>bugs.txt</code>.", parse_mode = "HTML")
	except:
		bot.send_message(cid, "El formato del comando es /bug *X* donde X es el mensaje que quieras enviar.", parse_mode = "Markdown")








@bot.message_handler(commands=['pb'])
def command_pb(message):
	ficha = "*" + "*\n [ ](" + "\n`PS`: " + "\n`Ataque` " + "\n`Defensa` " + "\n`Atk. Especial` " + "\n`Def. Especial` " + "\n`Velocidad` " + "\n`Total` " + "\n\n`Habilidad 1` " + "\n\n[" + " en Smogon](http://www.smogon.com/dex/xy/pokemon/" + ")"
	markup = types.InlineKeyboardMarkup()
	print("MENSAJE PRIMERO",message.message_id)
	markup.add(types.InlineKeyboardButton("result1", callback_data="data1"))
	bot.send_message(message.chat.id, 'Hihi'+ ficha, reply_markup=markup)
  






	@bot.callback_query_handler(func=lambda call: call.data == 'data1')
	def r1_call_back(call):
		editm = call.message.message_id
		markup = types.InlineKeyboardMarkup()
		markup.add(types.InlineKeyboardButton("result2", callback_data="data2"))
		print("MENSAJE SEGUNDO",editm)
		print(call.message.chat.id)

#		bot.send_message(call.message.chat.id, 'llego al comando')
#		bot.edit_message_text("pole menta", call.from_user.id, call.message.chat.id, call.message.message_id, reply_markup=markup)
		bot.edit_message_text(ficha, call.message.chat.id , editm, reply_markup=markup)
		#bot.send_message(call.message.chat.id, 'llego al comando')
		bot.answer_callback_query(call.id, text="") #Sale en pantalla
		#bot.send_message(call.message.chat.id, 'paso el comando')






@bot.callback_query_handler(func=lambda call: call.data == 'data2')
def r2_call_back(call):
	editm = call.message.message_id
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton("result1", callback_data="data1"))
	print("MENSAJE SEGUNDO",editm)
	print(call.message.chat.id)

#	bot.send_message(call.message.chat.id, 'llego al comando')
#	bot.edit_message_text("pole menta", call.from_user.id, call.message.chat.id, call.message.message_id, reply_markup=markup)
	bot.edit_message_text("Amapolas", call.message.chat.id , editm, reply_markup=markup)
	#bot.send_message(call.message.chat.id, 'llego al comando')
	bot.answer_callback_query(call.id, text="")
	#bot.send_message(call.message.chat.id, 'paso el comando')

@bot.callback_query_handler(func=lambda call: call.data == pkmn)
def r0_call_back(call):
	editm = call.message.message_id
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton("entra en el bueno", callback_data="data2"))
	print("MENSAJE SEGUNDO",editm)
	print(call.message.chat.id)

#	bot.send_message(call.message.chat.id, 'llego al comando')
#	bot.edit_message_text("pole menta", call.from_user.id, call.message.chat.id, call.message.message_id, reply_markup=markup)
	bot.edit_message_text("estoy en el bueno ", call.message.chat.id , editm, reply_markup=markup)
	#bot.send_message(call.message.chat.id, 'llego al comando')
	bot.answer_callback_query(call.id, text="") #Sale en pantalla
	#bot.send_message(call.message.chat.id, 'paso el comando')



tipos = {
	"steel":"Acero",
	"water":"Agua",
	"bug":"Bicho",
	"dragon":"Dragón",
	"electric":"Eléctrico",
	"ghost":"Fantasma",
	"fire":"Fuego",
	"fairy":"Hada",
	"ice":"Hielo",
	"fighting":"Lucha",
	"normal":"Normal",
	"grass":"Planta",
	"psychic":"Psíquico",
	"rock":"Roca",
	"dark":"Siniestro",
	"ground":"Tierra",
	"poison":"Veneno",
	"flying":"Volador"
}

#if "key" in tipos:
#
@bot.message_handler(commands=['array'])
def command_array(m):
	cid = m.chat.id
#	print(tipos.get)
#	print(list(map(tipos.get, tipos.keys())))
#	result = dict(zip(tipos.keys(), tipos.values()))
#	print(result.get("rock"))
	try: 
		poketipos = m.text.lower().split(' ', 1)[1]
		resultado = tipos.get(poketipos)
		print(resultado)
		bot.send_message(cid, resultado)
	except:
		None

#############################################
def poke_normal(pkmn):
	print("1) entro en la función de poke normal")
	print(pkmn)
	print("2) El poke con mayus es " + pkmn.capitalize())
	c.execute("SELECT Ndex,Nombre,Linkfoto,hp,atk,defe,atksp,defsp,spd,hab1,hab2,habo,tipo1,tipo2,evhp,evatk,evdefe,evatksp,evdefsp,evspd from POKEMON WHERE Nombre='" + str(pkmn)+ "'")
	for i in c:
		dex = i[0]
		name = i[1]
		imgpkm = i[2]
		hp = i[3]
		atk = i[4]
		defe = i[5]
		atksp = i[6]
		defsp = i[7]
		spd = i[8]
		hab1 = i[9]
		hab2 = i[10]
		habo = i[11]
		tipo1 = i[12]
		tipo2 = i[13]
		evhp = i[14]
		evatk = i[15]
		evdefe = i[16]
		evatksp = i[17]
		evdefsp = i[18]
		evspd = i[19]
		
	return dex, name,imgpkm, hp, atk, defe, atksp, defsp, spd, hab1, hab2, habo, tipo1, tipo2, evhp, evatk, evdefe, evatksp, evdefsp, evspd

def pintar_stats(hp, atk, defe, atksp, defsp, spd):
	
	if hp<=60:
		cbhp = "📕"
	elif (hp>60 and hp<=80):
		cbhp = "📙"
	elif (hp>80 and hp<=100):
		cbhp = "📒"
	elif hp>100:
		cbhp = "📗"
		
	if atk<=60:
		cbatk = "📕"
	elif (atk>60 and atk<=80):
		cbatk = "📙"
	elif (atk>80 and atk<=100):
		cbatk = "📒"

	elif atk>100:
		cbatk = "📗"

	if defe<=60:
		cbdefe = "📕"
	elif (defe>60 and defe<=80):
		cbdefe = "📙"
	elif (defe>80 and defe<=100):
		cbdefe = "📒"
	elif defe>100:
		cbdefe = "📗"

	if atksp<=60:
		cbatksp = "📕"
	elif (atksp>60 and atksp<=80):
		cbatksp = "📙"
	elif (atksp>80 and atksp<=100):
		cbatksp = "📒"
	elif atksp>100:
		cbatksp = "📗"
		
	if defsp<=60:
		cbdefsp = "📕"
	elif (defsp>60 and defsp<=80):
		cbdefsp = "📙"
	elif (defsp>80 and defsp<=100):
		cbdefsp = "📒"
	elif defsp>100:
		cbdefsp = "📗"
		
	if spd<=60:
		cbspd = "📕"
	elif (spd>60 and spd<=80):
		cbspd = "📙"
	elif (spd>80 and spd<=100):
		cbspd = "📒"
	elif spd>100:
		cbspd = "📗"
			
	return cbhp, cbatk, cbdefe, cbatksp, cbdefsp, cbspd
	
	
	
def pintar_tipo(tipo):
	etipo=""
	if(tipo == "Acero"):
		etipo = "  ⚙"
	elif(tipo == "Agua"):
		etipo = "   💦"
	elif(tipo == "Bicho"):
		etipo = "  🐛"
	elif(tipo == "Dragón"):
		etipo = "  🐉"
	elif(tipo == "Eléctrico"):
		etipo = "⚡️"
	elif(tipo == "Fantasma"):
		etipo = " 👻"
	elif(tipo == "Fuego"):
		etipo = "  🔥"
	elif(tipo == "Hada"):
		etipo = "   🎀"
	elif(tipo == "Hielo"):
		etipo = "  ❄️"
	elif(tipo == "Lucha"):
		etipo = "  💪"
	elif(tipo == "Normal"):
		etipo = "  🐕"
	elif(tipo == "Planta"):
		etipo = "  🍃"
	elif(tipo == "Psíquico"):
		etipo = " 🔮"
	elif(tipo == "Roca"):
		etipo = "   🗿"
	elif(tipo == "Siniestro"):
		etipo = "👤"
	elif(tipo == "Tierra"):
		etipo = "  🌎"
	elif(tipo == "Veneno"):
		etipo = "  🍄"
	elif(tipo == "Volador"):
		etipo = " 🌪"

	return etipo
	
@bot.message_handler(func=lambda m: m.text and (m.text.startswith("!stats") or m.text.startswith("/stats")))
def command_stats2(m):
#	global dex
	cid = m.chat.id
	pkmn = m.text.lower().split(' ', 1)[1].capitalize()
	print("3) AHORA TE PONGO EL POKE CAPITALISAO")
	print("4) " + pkmn)
	dex = 0
#	print(dex)
	name = ""
	imgpkm = ""
	hp = 0
	atk = 0
	defe = 0
	atksp = 0
	defsp = 0
	spd = 0
	hab1 = ""
	hab2 = ""
	habo = ""
	tipo1 = ""
	tipo2 = ""
	evhp = 0
	evatk = 0
	evdefe = 0
	evatksp = 0
	evdefsp =0
	evspd = 0
	cbhp = ""
	cbatk = ""
	cbdefe = ""
	cbatksp = ""
	cbdefsp = ""
	cbspd = ""
	etipo= ""
	habilidades= ""
	sname = ""
	flagr = 0
	

	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton("En desarollo", callback_data = "pkmn"))
	bot.send_chat_action(cid, "typing")
	nomega = ["venusaur", "blastoise", "charizard", "alakazam", "gengar", "kaaangaskhan", "pinsir", "gyarados", "aerodactyl", "mewtwo", "ampharos", "scizor", "heracross", "houndoom", "tyranitar", "blaziken", "gardevoir", "mawile", "aggron", "medichamp", "manectric", "banette", "absol", "garchomp", "lucario", "pidgeot", "sharpedo", "salamance", "abomasnow", "beedrill", "slowbro", "steelix", "sceptile", "swampert", "sableye", "camerut", "altaria", "glalie", "metagross", "latios", "latias", "rayquaza", "lopunny", "gallade", "audino", "diancie"]
	alolaform = ["Rattata", "Raticate", "Raichu", "Sandshrew", "Sandslash", "Vulpix", "Ninetales", "Diglett", "Dugtrio", "Meowth", "Persian", "Geodude", "Graveler", "Golem", "Grimer", "Muk", "Exeggutor", "Marowak"]

	
	try:
		if (m.text.lower().split(' ', 2)[2] == "mega"):
			npkmn = m.text.lower().split(' ', 2)[1]
			if(npkmn in nomega):
				print("5) Sé que pone mega y además tiene mega")
				bot.reply_to(m, "Las megas estarán pronto, ¡lo siento!", reply_markup=markup, parse_mode="Markdown")
				flagr = 1
			else:
				print("6) Sé que pone mega y este poke no tiene mega")
				bot.reply_to(m, "Este poke no tiene mega, pedazo troll", reply_markup=markup, parse_mode="Markdown")
				flagr =1
	except:
		print("7) NO HABIA SEGUNDA PALABRA EN MEGA")
	
	try:
		print("8) Voy a mirar si pone alola")
		if(m.text.lower().split(' ', 2)[2] == "alola"):
			npkmn = m.text.split(' ', 2)[1]
			npkmn = npkmn.capitalize()
			sppkmn = m.text.split(' ', 2)[2]
			sppkmn = sppkmn.capitalize()
			print(npkmn)
			if(npkmn in alolaform):
				print("9) Sé que pone alola y además tiene forma alola")
				npkmn = npkmn + " " + sppkmn
				dex, name,imgpkm, hp, atk, defe, atksp, defsp, spd, hab1, hab2, habo, tipo1, tipo2, evhp, evatk, evdefe, evatksp, evdefsp, evspd = poke_normal(npkmn)
				#dex = dex -10000
				t = hp + atk + defe + atksp + defsp + spd
				cbhp, cbatk, cbdefe, cbatksp, cbdefsp, cbspd = pintar_stats(hp, atk, defe, atksp, defsp, spd)
				etipo1 = pintar_tipo(tipo1)
#				etipo1 = etipo
				etipo2 = pintar_tipo(tipo2)
#				etipo2 = etipo
				print("Es de alola, pero... ¿Tiene habilidad 2?: " + hab2)
				if (((hab2 == " ") or (hab2 == "No tiene")) and ((habo == " ") or (habo == "No tiene"))):
					habilidades = "`Habilidad` " + str(hab1)
				elif ((habo == " ") or (habo == "No tiene")):
					habilidades = "`Habilidad 1` " + str(hab1) + "\n`Habilidad 2` " + str(hab2)
				elif ((hab2 == " ") or (hab2 == "No tiene")):
					habilidades = "`Habilidad 1` " + str(hab1) + "\n`Hab. Oculta` " + str(habo)
				else:
					habilidades = "`Habilidad 1` " + str(hab1) + "\n`Habilidad 2` " + str(hab2) + "\n`Hab. Oculta` " + str(habo)

				if (tipo2 is not " "):
					tipos = "`" + tipo1 + etipo1 + "`\n" + "`" + tipo2 + etipo2 + "`"
				else:
					tipos = tipo1 + etipo1
					
				if ")" in imgpkm:
					imgpkm = imgpkm
				else:
					imgpkm = imgpkm + ")"
		
				if "Código cero" in name:
					sname = "type\_null"
				elif "Lycanroc nocturno" in name:
					sname = "lycanroc-midnight"
				elif "Wishiwashi forma individual" in name:
					sname = "wishiwashi"
				elif "Minior forma meteorito" in name:
					sname = "minior"
				elif "Minior forma núcleo" in name:
					sname = "minior"
				elif " " in name:
					sname = name.replace(" ", "_")
				else:
					sname = name
				
				if len(dex) == 5:
					dex = dex[2:]
				else:
					dex = dex
					
#				bot.reply_to(m,
#				"_#" + dex + "_ - " + "*" + name + "*\n" + tipos + "\n\n`PS`: " + str(cbhp) + str(hp) +
#				"\n`Ataque` " + str(cbatk) + str(atk) + "\n`Defensa` " + str(cbdefe)+ str(defe) + "\n`Atk. Esp.` " + str(cbatksp) + str(atksp) + 
#				"\n`Def. Esp.` " + str(cbdefsp) + str(defsp) + "\n`Velocidad` " + str(cbspd) + str(spd) + "\n`Total` " + str(t) + 
#				"\n\n" + habilidades + "\n" + "[ ](" + imgpkm
#				+ "\n["+name+ " en Smogon](http://www.smogon.com/dex/sm/pokemon/" + sname + ")", parse_mode = "Markdown")




################{}.format -> f"{a}"############################"



#				bot.reply_to(m, f"_# {dex}_ - *{name}*\n{tipos}\n\n`PS`: str(cbhp}{hp}\n`Ataque`: {cbatk}{atk}\n`Defensa`: {cbdefe}{defe}\n`Atk. Esp.`: {cbatksp}{atksp}\n`Def. Esp.`: {cbdefsp}{defsp}\n`Velocidad`: {cbspd}{spd}\n`Total`: {t}\n\n{habilidades}\n[ ]({imgpkm}\n[{name} en Smogon](http://www.smogon.com/dex/sm/pokemon/{sname})", parse_mode = "Markdown")
#				bot.reply_to(m, """
#				_# {dex}_ - *{name}*\n{tipos}\n\n`PS`: {cbhp}{hp}
#				\n`Ataque`: {cbatk}{atk}\n`Defensa`: {cbdefe}{defe}\n`Atk. Esp.`: {cbatksp}{atksp}
#				\n`Def. Esp.`: {cbdefsp}{defsp}\n`Velocidad`: {cbspd}{spd}\n`Total`: {t}
#				\n\n{habilidades}\n[ ]({imgpkm}
#				\n[{name} en Smogon](http://www.smogon.com/dex/sm/pokemon/{sname})"""
#				.format(dex, name, tipos, cbhp, hp, cbatk, atk, cbdef, defe, cbatksp, atksp, cbdefsp, defsp, cbspd, spd, t, habilidades, imgpkmn, sname), parse_mode = "Markdown")


				ficha = "_# {0}_ - *{1}*\n{2}\n\n`PS:` {3}{4}\n`Ataque:` {5}{6}\n`Defensa:` {7}{8}\n`Atk. Esp.:` {9}{10}\n`Def. Esp.:` {11}{12}\n`Velocidad:` {13}{14}\n`Total:` {15}\n\n{16}\n[ ]({17}\n[{1} en Smogon](http://www.smogon.com/dex/sm/pokemon/{18})"
				bot.reply_to(m, ficha.format(dex, name, tipos, cbhp, hp, cbatk, atk, cbdefe, defe, cbatksp, atksp, cbdefsp, defsp, cbspd, spd, t, habilidades, imgpkm, sname), parse_mode = "Markdown")


				print("_#" + dex + "_ - " + "*" + name + "*\n" + tipos + "\n\n`PS`: " + str(cbhp) + str(hp) +"\n`Ataque` " + str(cbatk) + str(atk) + "\n`Defensa` " + str(cbdefe)+ str(defe) + "\n`Atk. Esp.` " + str(cbatksp) + str(atksp) + "\n`Def. Esp.` " + str(cbdefsp) + str(defsp) + "\n`Velocidad` " + str(cbspd) + str(spd) + "\n`Total` " + str(t) + "\n\n" + habilidades + "\n" + "[ ](" + imgpkm + "\n\n["+name+ " en Smogon](http://www.smogon.com/dex/sm/pokemon/" + name + ")")

				flagr = 2
			else:
				print("11) Sé que pone alola y este poke no tiene forma alola")
				bot.reply_to(m, "Este poke no tiene forma alola, pedazo troll", reply_markup=markup, parse_mode="Markdown")
				flagr = 2
				
	except:
		print("12) NO HABIA SEGUNDA PALABRA EN ALOLA")
	try:
		if(flagr == 0):
			print("13) No pone mega ni pone alola")
		#		sppkmn = m.text.split(' ', 2)[2]
		#		sppkmn = sppkmn.capitalize()
			dex, name,imgpkm, hp, atk, defe, atksp, defsp, spd, hab1, hab2, habo, tipo1, tipo2, evhp, evatk, evdefe, evatksp, evdefsp, evspd = poke_normal(pkmn)
			t = hp + atk + defe + atksp + defsp + spd
			cbhp, cbatk, cbdefe, cbatksp, cbdefsp, cbspd = pintar_stats(hp, atk, defe, atksp, defsp, spd)
			etipo1 = pintar_tipo(tipo1)
		#	etipo1 = etipo
			etipo2 = pintar_tipo(tipo2)
		#	etipo2 = etipo
	#		if (((hab2 is not " ") or (hab2 is not "No tiene")) and ((habo is not " ") or (habo is not "No tiene"))):
	#			habilidades = "`Habilidad 1` " + str(hab1) + "\n`Habilidad 2` " + str(hab2) + "\n`Hab. Oculta` " + str(habo)
	#		elif ((hab2 is not " ") or (hab2 is not "No tiene")):
	#			habilidades = "`Habilidad 1` " + str(hab1) + "\n`Habilidad 2` " + str(hab2)
	#		elif ((habo is not " ") or (habo is not "No tiene")):
	#			habilidades = "`Habilidad 1` " + str(hab1) + "\n`Hab. Oculta` " + str(habo)
	#		else:
	#			habilidades = "`Habilidad` " + str(hab1)
			print("¿Tiene habilidad 2?: " + hab2)
			if (((hab2 == " ") or (hab2 == "No tiene")) and ((habo == " ") or (habo == "No tiene"))):
				habilidades = "`Habilidad` " + str(hab1)
			elif ((habo == " ") or (habo == "No tiene")):
				habilidades = "`Habilidad 1` " + str(hab1) + "\n`Habilidad 2` " + str(hab2)
			elif ((hab2 == " ") or (hab2 == "No tiene")):
				habilidades = "`Habilidad 1` " + str(hab1) + "\n`Hab. Oculta` " + str(habo)
			else:
				habilidades = "`Habilidad 1` " + str(hab1) + "\n`Habilidad 2` " + str(hab2) + "\n`Hab. Oculta` " + str(habo)
				
				
			if (tipo2 is not " "):
				tipos = "`" + tipo1 + etipo1 + "`\n" + "`" + tipo2 + etipo2 + "`"
			else:
				tipos = tipo1 + etipo1
				
			if ")" in imgpkm:
				imgpkm = imgpkm
			else:
				imgpkm = imgpkm + ")"
	
			if "Código cero" in name:
				sname = "type\_null"
			elif "Lycanroc nocturno" in name:
				sname = "lycanroc-midnight"
			elif "Wishiwashi forma individual" in name:
				sname = "wishiwashi"
			elif "Minior forma meteorito" in name:
				sname = "minior"
			elif "Minior forma núcleo" in name:
				sname = "minior"
			elif " " in name:
				sname = name.replace(" ", "_")
			else:
				sname = name
			
			if len(dex) == 5:
				dex = dex[2:]
			else:
				dex = dex


			ficha = "_# {0}_ - *{1}*\n{2}\n\n`PS:` {3}{4}\n`Ataque:` {5}{6}\n`Defensa:` {7}{8}\n`Atk. Esp.:` {9}{10}\n`Def. Esp.:` {11}{12}\n`Velocidad:` {13}{14}\n`Total:` {15}\n\n{16}\n[ ]({17}\n[{1} en Smogon](http://www.smogon.com/dex/sm/pokemon/{18})"
			bot.reply_to(m, ficha.format(dex, name, tipos, cbhp, hp, cbatk, atk, cbdefe, defe, cbatksp, atksp, cbdefsp, defsp, cbspd, spd, t, habilidades, imgpkm, sname), parse_mode = "Markdown")


			#bot.reply_to(m,
			#"_#" + dex + "_ - " + "*" + name + "*\n" + tipos + "\n\n`PS`: " + str(cbhp) + str(hp) +
			#"\n`Ataque` " + str(cbatk) + str(atk) + "\n`Defensa` " + str(cbdefe)+ str(defe) + "\n`Atk. Esp.` " + str(cbatksp) + str(atksp) + 
			#"\n`Def. Esp.` " + str(cbdefsp) + str(defsp) + "\n`Velocidad` " + str(cbspd) + str(spd) + "\n`Total` " + str(t) + 
			#"\n\n" + habilidades + "\n" + "[ ](" + imgpkm
			#+ "\n["+name+ " en Smogon](http://www.smogon.com/dex/sm/pokemon/" + sname + ")", parse_mode = "Markdown")
			print("_#" + dex + "_ - " + "*" + name + "*\n" + tipos + "\n\n`PS`: " + str(cbhp) + str(hp) +"\n`Ataque` " + str(cbatk) + str(atk) + "\n`Defensa` " + str(cbdefe)+ str(defe) + "\n`Atk. Esp.` " + str(cbatksp) + str(atksp) + "\n`Def. Esp.` " + str(cbdefsp) + str(defsp) + "\n`Velocidad` " + str(cbspd) + str(spd) + "\n`Total` " + str(t) + "\n\n" + habilidades + "\n" + "[ ](" + imgpkm + "\n\n["+name+ " en Smogon](http://www.smogon.com/dex/sm/pokemon/" + name + ")")
	except:
		bot.reply_to(m, "Introduce un pokémon, por favor.")


bot.skip_pending = True		
bot.polling(none_stop=True)
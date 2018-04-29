# -*- coding: utf-8 -*-

import json
import codecs
import requests
import bs4
from bs4 import BeautifulSoup, SoupStrainer
import re
import subprocess
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater
from html import escape
from registrationModule import registerUser


from babel.numbers import format_currency
import requests

updater = Updater(token='593637956:AAH3WOco3wjCmznOLl2gcTKzAH4BMG0CF8I')
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

def commands(bot, update):
	user = update.message.from_user.username
	bot.send_message(chat_id=update.message.chat_id, text="Initiating commands /tip & /withdraw have a specfic format,\n use them like so:" + "\n \n Parameters: \n <user> = target user to tip \n <amount> = amount of rupeecoin to utilise \n <address> = rupeecoin address to withdraw to \n \n Tipping format: \n /tip <user> <amount> \n \n Withdrawing format: \n /withdraw <address> <amount>")

def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="The following commands are at your disposal: /hi , /commands , /deposit , /tip , /withdraw , /price , /marketcap or /balance")

def register_user(bot, update):
	# Get UserName
	user = update.message.from_user.username

	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		address, registered = registerUser(user)
		if registered:
			bot.send_message(chat_id=update.message.chat_id, text="@{0} your depositing tipbot address is: {1}".format(user,address))
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")

def deposit(bot, update):
	user = update.message.from_user.username
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		address = "/usr/local/bin/rupeed"
		process = subprocess.Popen([address,"getaccountaddress",user],stdout=subprocess.PIPE)
		stdout, result = process.communicate()
		clean = (stdout.strip()).decode("utf-8")
		bot.send_message(chat_id=update.message.chat_id, text="@{0} your depositing address is: {1}".format(user,clean))
		registerUser(user,clean)

def tip(bot,update):
	user = update.message.from_user.username
	target = "@siddimore"
	# target = update.message.text[5:]
	# amount =  target.split(" ")[1]
	# target =  target.split(" ")[0]
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		machine = "@Rupee_bot"
		if target == machine:
			bot.send_message(chat_id=update.message.chat_id, text="HODL.")
		elif "@" in target:
			target = target[1:]
			user = update.message.from_user.username
<<<<<<< HEAD
			address, registered = registerUser(user)
			print(address)
			bot.send_message(chat_id=update.message.chat_id, text="@{0} your Tipping Wallet Address is {1}.".format(user, address))
			# core = "/usr/local/bin/reddcoind"
			# result = subprocess.run([core,"getbalance",user],stdout=subprocess.PIPE)
			# balance = float((result.stdout.strip()).decode("utf-8"))
			# amount = float(amount)
			# if balance < amount:
			# 	bot.send_message(chat_id=update.message.chat_id, text="@{0} you have insufficent funds.".format(user))
			# elif target == user:
			# 	bot.send_message(chat_id=update.message.chat_id, text="You can't tip yourself silly.")
			# else:
			# 	balance = str(balance)
			# 	amount = str(amount)
			# 	tx = subprocess.run([core,"move",user,target,amount],stdout=subprocess.PIPE)
			# 	bot.send_message(chat_id=update.message.chat_id, text="@{0} tipped @{1} of {2} RDD".format(user, target, amount))
=======
			core = "/usr/local/bin/rupeed"
			result = subprocess.run([core,"getbalance",user],stdout=subprocess.PIPE)
			balance = float((result.stdout.strip()).decode("utf-8"))
			amount = float(amount)
			if balance < amount:
				bot.send_message(chat_id=update.message.chat_id, text="@{0} you have insufficent funds.".format(user))
			elif target == user:
				bot.send_message(chat_id=update.message.chat_id, text="You can't tip yourself silly.")
			else:
				balance = str(balance)
				amount = str(amount)
				tx = subprocess.run([core,"move",user,target,amount],stdout=subprocess.PIPE)
				bot.send_message(chat_id=update.message.chat_id, text="@{0} tipped @{1} of {2} RDD".format(user, target, amount))
>>>>>>> 3010d9972734d543aadfb0863cdacdf259657938
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Error that user is not applicable.")

def balance(bot,update):
	quote_page = requests.get('https://www.worldcoinindex.com/coin/rupeecoin')
	strainer = SoupStrainer('div', attrs={'class': 'row mob-coin-table'})
	soup = BeautifulSoup(quote_page.content, 'html.parser', parse_only=strainer)
	name_box = soup.find('div', attrs={'class':'col-md-6 col-xs-6 coinprice'})
	name = name_box.text.replace("\n","")
	price = re.sub(r'\n\s*\n', r'\n\n', name.strip(), flags=re.M)
	price = re.sub("[^0-9^.]", "", price)
	price = float(price)
	user = update.message.from_user.username
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		core = "/usr/local/bin/rupeed"
		result = subprocess.run([core,"getbalance",user],stdout=subprocess.PIPE)
		clean = (result.stdout.strip()).decode("utf-8")
		balance  = float(clean)
		fiat_balance = balance * price
		fiat_balance = str(round(fiat_balance,3))
		balance =  str(round(balance,3))
		bot.send_message(chat_id=update.message.chat_id, text="@{0} your current balance is: {1} RDD ≈  ${2}".format(user,balance,fiat_balance))

def price(bot,update):
	quote_page = requests.get('https://www.worldcoinindex.com/coin/rupee')
	strainer = SoupStrainer('div', attrs={'class': 'row mob-coin-table'})
	soup = BeautifulSoup(quote_page.content, 'html.parser', parse_only=strainer)
	name_box = soup.find('div', attrs={'class':'col-md-6 col-xs-6 coinprice'})
	name = name_box.text.replace("\n","")
	price = re.sub(r'\n\s*\n', r'\n\n', name.strip(), flags=re.M)
	fiat = soup.find('span', attrs={'class': ''})
	kkz = fiat.text.replace("\n","")
	percent = re.sub(r'\n\s*\n', r'\n\n', kkz.strip(), flags=re.M)
	quote_page = requests.get('https://bittrex.com/api/v1.1/public/getticker?market=btc-rdd')
	soup = BeautifulSoup(quote_page.content, 'html.parser').text
	btc = soup[80:]
	sats = btc[:-2]
	bot.send_message(chat_id=update.message.chat_id, text="RupeeCoin is valued at {0} Δ {1} ≈ {2}".format(price,percent,sats) + " ฿")

def withdraw(bot,update):
	user = update.message.from_user.username
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		target = update.message.text[9:]
		address = target[:35]
		address = ''.join(str(e) for e in address)
		target = target.replace(target[:35], '')
		amount = float(target)
		core = "/usr/local/bin/rupeed"
		result = subprocess.run([core,"getbalance",user],stdout=subprocess.PIPE)
		clean = (result.stdout.strip()).decode("utf-8")
		balance = float(clean)
		if balance < amount:
			bot.send_message(chat_id=update.message.chat_id, text="@{0} you have insufficent funds.".format(user))
		else:
			amount = str(amount)
			tx = subprocess.run([core,"sendfrom",user,address,amount],stdout=subprocess.PIPE)
			bot.send_message(chat_id=update.message.chat_id, text="@{0} has successfully withdrew to address: {1} of {2} RDD" .format(user,address,amount))

def hi(bot,update):
	user = update.message.from_user.username
	bot.send_message(chat_id=update.message.chat_id, text="Hello @{0}, how are you doing today?".format(user))

def moon(bot,update):
  bot.send_message(chat_id=update.message.chat_id, text="Moon mission inbound!")

def marketcap(bot,update):
	r = requests.get('https://api.coinmarketcap.com/v1/ticker/rupee/')
	for coin in r.json():
	    print(coin["market_cap_usd"])
	market_cap = format_currency(coin["market_cap_usd"], 'USD', locale='en_US')
	bot.send_message(chat_id=update.message.chat_id, text="The current market cap of Ruppee is valued at {0}".format(market_cap))

from telegram.ext import CommandHandler

commands_handler = CommandHandler('commands', commands)
dispatcher.add_handler(commands_handler)

moon_handler = CommandHandler('moon', moon)
dispatcher.add_handler(moon_handler)

hi_handler = CommandHandler('hi', hi)
dispatcher.add_handler(hi_handler)

withdraw_handler = CommandHandler('withdraw', withdraw)
dispatcher.add_handler(withdraw_handler)

marketcap_handler = CommandHandler('marketcap', marketcap)
dispatcher.add_handler(marketcap_handler)

deposit_handler = CommandHandler('deposit', deposit)
dispatcher.add_handler(deposit_handler)

price_handler = CommandHandler('price', price)
dispatcher.add_handler(price_handler)

tip_handler = CommandHandler('tip', tip)
dispatcher.add_handler(tip_handler)

balance_handler = CommandHandler('balance', balance)
dispatcher.add_handler(balance_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

help_handler = CommandHandler('register', register_user)
dispatcher.add_handler(help_handler)

updater.start_polling()

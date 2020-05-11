from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import requests
import re
import json
import time
import os

TOKEN = "1156469077:AAGZvfC8XwNm7nqFUBvBhw6n2gYq1nb4WC4"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
PORT = int(os.environ.get('PORT', 5000))

def location(bot, update):
    try:
        loc = update.message.location
        contents = requests.post('https://data.geoiq.io/dataapis/v1.0/covid/locationcheck',json={'key':"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtYWlsSWRlbnRpdHkiOiJjaGF2YW5zYW5pa2F2aWthc0BnbWFpbC5jb20ifQ.9GhEC_MyTUHxiB7hWQ1HowI7QjrRuiD_yaO8cEUl008",'latlngs':[[loc['latitude'],loc['longitude']]]}).json()
        url = contents['data'][0]['inContainmentZone']
        print(url)
        if url == True:
            text = "Unfortunately, your location falls under the containment region. "+"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
        else:
            text = "Congratulations, your location doesnt fall under the containment region." +"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
        update.message.reply_text(text)
        update.message.reply_text("Type /thanks if done.")
    except Exception as e:
        print(e)
    
def containmentzone(bot, update):
    try:
        update.message.reply_text("Please send your location.")
    except Exception as e:
        print(e)
        
def start(bot, update):
    try:
        text = "Hello "+update["message"]["chat"]["first_name"].capitalize()+"! My Name is CovidCare Bot. I can help you by letting you know if your location falls under a containment zone. Type /containmentzone to know."
        update.message.reply_text(text)
    except Exception as e:
        print(e) 
    
def thanks(bot, update):
    try:
        text = "You're Welcome "+update["message"]["chat"]["first_name"].capitalize()+"! Carry On."
        update.message.reply_text(text)
    except Exception as e:
        print(e) 
def echo(bot, update):
    try:
        text = "I'm sorry, I'm afraid I can't provide information for this."
        update.messaage.reply_text(text)
    except Exception as e:
        print(e)    

def main():
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("thanks", thanks))
    dp.add_handler(CommandHandler("containmentzone", containmentzone))
    dp.add_handler(MessageHandler(Filters.location, location))
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
    updater.bot.setWebhook('https://warm-sands-70860.herokuapp.com/' + TOKEN)
if __name__ == '__main__':
    main()

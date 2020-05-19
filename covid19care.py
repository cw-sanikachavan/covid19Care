from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import requests
import itertools  
import re
import json
import time
import os
import telegram
from geopy.distance import geodesic
import gspread
from covid import Covid

TOKEN = "1156469077:AAGZvfC8XwNm7nqFUBvBhw6n2gYq1nb4WC4"
t = "1115904035:AAG5x0dpPwmYNKRNBIHfjN7iADHTU4VN6UE"
PORT = int(os.environ.get('PORT', 5000))
LIVE_UPDATES, MENU, SET_STAT, CONTAINMENTZONE, TESTINGCENTERS, ECHO, SYMPTOMS, SAFETY = range(8)
STATE = SET_STAT
def live_updates(bot,update):
    try:
        covid = Covid()
        data = covid.get_status_by_country_name("india")
        update.message.reply_text("Total Confirmed cases in India are: "+str(data['confirmed'])+"\nTotal Active cases in India are: "+ str(data['active'])+"\nTotal Recovered cases in India are: "+ str(data['recovered'])+"\nTotal Deceased cases in India are: "+ str(data['deaths']))
        update.message.reply_text("Type /thanks if done or /menu to select another option.")
    except Exception as e:
        print(e)
        
def symptoms(bot, update):
    try:              
        update.message.reply_text("Common-Symptoms: \n1.Fever \n2.Tiredness \n3.Dry Cough \n\nAdditional-Symptoms: \n1.Aches And Pains \n2.Nasal Congestion \n3.Runny Nose \n4.Sore Throat \n5.Diarrhoea")
        update.message.reply_text("Type /thanks if done or /menu to select another option.")
    except Exception as e:
        print(e)
        
def safety(bot, update):
    try:              
        update.message.reply_text("Safety Facts: \n1.Clean your hands often. Use soap and water, or an alcohol-based hand rub. \n2.Maintain a safe distance from anyone who is coughing or sneezing. \n3.Don\u2019t touch your eyes, nose or mouth. \n4.Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze. \n5.Stay home if you feel unwell. \n6.If you have a fever, a cough, and difficulty breathing, seek medical attention. Call in advance. \n7.Follow the directions of your local health authority.")
        update.message.reply_text("Type /thanks if done or /menu to select another option.")
    except Exception as e:
        print(e)

def containmentzone(bot, update):
    try:
        print("bye")
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        loc = update.message.location
        contents = requests.post('https://data.geoiq.io/dataapis/v1.0/covid/locationcheck',json={'key':"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtYWlsSWRlbnRpdHkiOiJjaGF2YW5zYW5pa2F2aWthc0BnbWFpbC5jb20ifQ.9GhEC_MyTUHxiB7hWQ1HowI7QjrRuiD_yaO8cEUl008",'latlngs':[[loc['latitude'],loc['longitude']]]}).json()
        url = contents['data'][0]['inContainmentZone']
        print(url)
        if url == True:
            text = "Unfortunately, your location falls under the containment region. "+"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
        else:
            text = "Congratulations, your location doesnt fall under the containment region." +"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
        update.message.reply_text(text)
        update.message.reply_text("Type /thanks if done or /menu to select another option.")
    except Exception as e:
        print(e)

def testingcenters(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        lstF = []
        loc = update.message.location
        user_lat = loc.latitude
        user_long = loc.longitude
        locTup = (user_lat,user_long)
        gc = gspread.service_account(filename='service_account.json')
        worksheet = gc.open('FinalSheet').sheet1
        types = worksheet.col_values(3)
        hospitals = worksheet.col_values(4)
        latitude = worksheet.col_values(5)
        longitude = worksheet.col_values(6)
        for (a, b, c, d) in zip(types, hospitals, latitude, longitude):
            hospTup = (c,d)
            dist = geodesic(locTup, hospTup).miles
            finalTup = (a,b,dist)
            lstF.append(finalTup)
        sLst = sorted(lstF,key = lambda x: x[2])
        update.message.reply_text("The 5 closest testing centers to your location are:")
        for i in range(1,6):
            update.message.reply_text(str(i)+". "+sLst[i][1]+" Type: "+sLst[i][0])
        update.message.reply_text("Type /thanks if done or /menu to select another option.")
    except Exception as e:
        print(e)

def menu(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        keyboard = [['Containment_Zone', 'Testing_Centers','Symptoms','Safety_Measures','Live_Updates']]

        reply_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
        update.message.reply_text("Select an option to continue.", reply_markup=reply_markup)
        return SET_STAT
    except Exception as e:
        print(e)
    
def servicetype(bot, update):
    try:
        global STATE
        TYPE = update.message.text
        print(TYPE)
        print(update.message.text)
        if update.message.text == 'Containment_Zone':
            print('c')
            STATE = CONTAINMENTZONE
            request_location(bot,update)
            return CONTAINMENTZONE
        elif update.message.text == 'Testing_Centers':
            print('t')
            STATE = TESTINGCENTERS
            request_location(bot,update)
            return TESTINGCENTERS
        elif update.message.text == 'Symptoms':
            print('sy')
            STATE = SYMPTOMS
            symptoms(bot, update)
            return MENU
        elif update.message.text == 'Safety_Measures':
            print('sf')
            STATE = SAFETY
            safety(bot, update)
            return MENU
        elif update.message.text == 'Live_Updates':
            print('l')
            STATE = LIVE_UPDATES
            live_updates(bot,update)
            return MENU
        else:
            STATE = MENU
            return MENU
    except Exception as e:
        print(e)
        
def request_location(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        update.message.reply_text("Please send your location.")
        return
    except Exception as e:
        print(e)
        
def start(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        keyboard = [['Containment_Zone', 'Testing_Centers','Symptoms','Safety_Measures','Live_Updates']]
        text = "Hello "+update["message"]["chat"]["first_name"].capitalize()+"! My Name is CovidCare Bot. I can help you by letting you know if your location falls under a containment zone. Select an option to continue."
        update.message.reply_text(text,reply_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True))
        return SET_STAT
    except Exception as e:
        print(e) 
    
def thanks(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        text = "You're Welcome "+update["message"]["chat"]["first_name"].capitalize()+"! Carry On."
        update.message.reply_text(text)
    except Exception as e:
        print(e) 
def echo(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        text = "I'm sorry, I'm afraid I can't provide information for this."
        update.messaage.reply_text(text)
    except Exception as e:
        print(e)    

def main():
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SET_STAT: [RegexHandler('^(Containment_Zone|Testing_Centers|Symptoms|Safety_Measures|Live_Updates)$',servicetype )],
            MENU: [CommandHandler('menu', menu)],
            CONTAINMENTZONE: [MessageHandler(Filters.location, containmentzone)],
            TESTINGCENTERS: [MessageHandler(Filters.location, testingcenters)],
            ECHO:[MessageHandler(Filters.text,echo)]
             },
        fallbacks=[CommandHandler('thanks', thanks)]
    )

    dp.add_handler(conv_handler)
    #updater.start_polling()
    #updater.idle()
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
    updater.bot.setWebhook('https://quiet-escarpment-71463.herokuapp.com/' + TOKEN)
if __name__ == '__main__':
    main()

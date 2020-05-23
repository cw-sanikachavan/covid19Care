from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import requests, itertools, re, json, time, os, telegram
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from covid import Covid
import pandas as pd

TOKEN = "1156469077:AAGZvfC8XwNm7nqFUBvBhw6n2gYq1nb4WC4"
t = "1115904035:AAG5x0dpPwmYNKRNBIHfjN7iADHTU4VN6UE"
PORT = int(os.environ.get('PORT', 5000))
LIVE_UPDATES, MENU, SET_STAT, CONTAINMENTZONE, TESTINGCENTERS, HELPLINE_NUMBER, CONTAINMENTZONER, SAFETY, SYMPTOMS, THANKS = range(10)
STATE = SET_STAT
user_lat = 0
user_long = 0

def helplinenumber(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        lstF = []
        loc = update.message.location
        global user_lat
        user_lat = loc.latitude
        global user_long
        user_long = loc.longitude
        locTup = (user_lat,user_long)
        worksheet = pd.read_csv('coronvavirushelplinenumber.csv')
        state = worksheet['State'].tolist()
        helplineNos = worksheet['Helpline Nos.'].tolist()
        geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        location = geolocator.reverse(str(user_lat)+", "+str(user_long))
        dataL = location.raw
        district = dataL['address']['state_district']
        stateL = dataL['address']['state']
        print(district,stateL)
        for (a,b) in zip(state, helplineNos):
            if stateL==a:
                print(a,b)
                update.message.reply_text("Central Helpline Number: +91-11-23978046 and Toll Free: 1075 \nHelpline Email ID: ncov2019@gov.in")
                update.message.reply_text("Helpline Number for "+a+" is "+str(b))
                update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return SET_STAT
    except Exception as e:
        print(e)    
        update.message.reply_text("Service Timed Out. Please press start to continue.")

def helplinenumberR(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        lstF = []
        #loc = update.message.location
        #user_lat = loc.latitude
        #user_long = loc.longitude
        locTup = (user_lat,user_long)
        worksheet = pd.read_csv('coronvavirushelplinenumber.csv')
        state = worksheet['State'].tolist()
        helplineNos = worksheet['Helpline Nos.'].tolist()
        geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        location = geolocator.reverse(str(user_lat)+", "+str(user_long))
        dataL = location.raw
        district = dataL['address']['state_district']
        stateL = dataL['address']['state']
        print(district,stateL)
        for (a,b) in zip(state, helplineNos):
            if stateL==a:
                print(a,b)
                update.message.reply_text("Central Helpline Number: +91-11-23978046 and Toll Free: 1075 \nHelpline Email ID: ncov2019@gov.in")
                update.message.reply_text("Helpline Number for "+a+" is "+str(b))
                update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return
    except Exception as e:
        print(e)    
        update.message.reply_text("Service Timed Out. Please press start to continue.")

def immunity_boost(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        bot.send_photo(chat_id=update.message.chat.id, photo="https://www.ayush.gov.in/img/m2.jpeg")
        bot.send_photo(chat_id=update.message.chat.id, photo="https://www.ayush.gov.in/img/m3.jpeg")
        bot.send_photo(chat_id=update.message.chat.id, photo="https://www.ayush.gov.in/img/m4.jpeg")
        update.message.reply_text("Source: https://www.ayush.gov.in/")
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return 
    except Exception as e:
        print(e)
        update.message.reply_text("Service Timed Out. Please press start to continue.")

    
def myth_buster(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        bot.send_document(chat_id=update.message.chat.id, document=open("MythsVsFacts.pdf","rb"))
        update.message.reply_text("Source: MyGov Corona Hub FB Page")
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return 
    except Exception as e:
        print(e)
        update.message.reply_text("Service Timed Out. Please press start to continue.")
    
def live_updates(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        covid = Covid()
        data = covid.get_status_by_country_name("india")
        global user_lat
        global user_long
        loc = update.message.location
        user_lat = loc.latitude
        user_long = loc.longitude
        stateR = 0
        stateA = 0
        stateC = 0
        stateD = 0
        geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        location = geolocator.reverse(str(user_lat)+", "+str(user_long))
        dataL = location.raw
        district = dataL['address']['state_district']
        state = dataL['address']['state']
        if district == "Mumbai Suburban":
            district = "Mumbai"
        js = requests.get("https://api.covid19india.org/v2/state_district_wise.json").json()
        for i in js:
            if state == i['state']:
                for j in i['districtData']:
                    stateA = stateA + j['active']
                    stateR = stateR + j['recovered']
                    stateC= stateC + j['confirmed']
                    stateD = stateD + j['deceased']
                    if j['district'] == district:
                        text = "Total Confirmed cases in "+district+" are: "+str(j['confirmed'])+"\nTotal Active cases in "+district+" are: "+ str(j['active'])+"\nTotal Recovered cases in "+district+" are: "+ str(j['recovered'])+"\nTotal Deaths cases in "+district+" are: "+ str(j['deceased'])+"\nRecovery Rate in "+district+":"+str(round(j['recovered']/j['confirmed'],2))+"\nMortality Rate in "+district+":"+str(round(j['deceased']/j['confirmed'],2))
                        print(str(j['confirmed']))
        update.message.reply_text("Total Confirmed cases in India are: "+str(data['confirmed'])+"\nTotal Active cases in India are: "+ str(data['active'])+"\nTotal Recovered cases in India are: "+ str(data['recovered'])+"\nTotal Deaths cases in India are: "+ str(data['deaths'])+"\nRecovery Rate in India:"+str(round(data['recovered']/data['confirmed'],2))+"\nMortality Rate in India:"+str(round(data['deaths']/data['confirmed'],2)))
        update.message.reply_text("Total Confirmed cases in "+state+" are: "+str(stateC)+"\nTotal Active cases in "+state+" are: "+ str(stateA)+"\nTotal Recovered cases in "+state+" are: "+ str(stateR)+"\nTotal Deaths cases in "+state+" are: "+ str(stateD)+"\nRecovery Rate in "+state+":"+str(round(stateR/stateC,2))+"\nMortality Rate in "+state+":"+str(round(stateD/stateC,2)))
        update.message.reply_text(text)
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return SET_STAT
    except Exception as e:
        print(e)
        update.message.reply_text("Service Timed Out. Please press start to continue.")

def live_updatesR(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        covid = Covid()
        data = covid.get_status_by_country_name("india")
        #loc = update.message.location
        #user_lat = loc.latitude
        #user_long = loc.longitude
        stateR = 0
        stateA = 0
        stateC = 0
        stateD = 0
        geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        location = geolocator.reverse(str(user_lat)+", "+str(user_long))
        dataL = location.raw
        district = dataL['address']['state_district']
        state = dataL['address']['state']
        if district == "Mumbai Suburban":
            district = "Mumbai"
        js = requests.get("https://api.covid19india.org/v2/state_district_wise.json").json()
        for i in js:
            if state == i['state']:
                for j in i['districtData']:
                    stateA = stateA + j['active']
                    stateR = stateR + j['recovered']
                    stateC= stateC + j['confirmed']
                    stateD = stateD + j['deceased']
                    if j['district'] == district:
                        text = "Total Confirmed cases in "+district+" are: "+str(j['confirmed'])+"\nTotal Active cases in "+district+" are: "+ str(j['active'])+"\nTotal Recovered cases in "+district+" are: "+ str(j['recovered'])+"\nTotal Deaths cases in "+district+" are: "+ str(j['deceased'])+"\nRecovery Rate in "+district+":"+str(round(j['recovered']/j['confirmed'],2))+"\nMortality Rate in "+district+":"+str(round(j['deceased']/j['confirmed'],2))
                        print(str(j['confirmed']))
        update.message.reply_text("Total Confirmed cases in India are: "+str(data['confirmed'])+"\nTotal Active cases in India are: "+ str(data['active'])+"\nTotal Recovered cases in India are: "+ str(data['recovered'])+"\nTotal Deaths cases in India are: "+ str(data['deaths'])+"\nRecovery Rate in India:"+str(round(data['recovered']/data['confirmed'],2))+"\nMortality Rate in India:"+str(round(data['deaths']/data['confirmed'],2)))
        update.message.reply_text("Total Confirmed cases in "+state+" are: "+str(stateC)+"\nTotal Active cases in "+state+" are: "+ str(stateA)+"\nTotal Recovered cases in "+state+" are: "+ str(stateR)+"\nTotal Deaths cases in "+state+" are: "+ str(stateD)+"\nRecovery Rate in "+state+":"+str(round(stateR/stateC,2))+"\nMortality Rate in "+state+":"+str(round(stateD/stateC,2)))
        update.message.reply_text(text)
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return
    except Exception as e:
        print(e)
        update.message.reply_text("Service Timed Out. Please press start to continue.")

def symptoms(bot, update):
    try:              
        update.message.reply_text("Common-Symptoms: \n1.Fever \n2.Tiredness \n3.Dry Cough \n\nAdditional-Symptoms: \n1.Aches And Pains \n2.Nasal Congestion \n3.Runny Nose \n4.Sore Throat \n5.Diarrhoea")
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return 
    except Exception as e:
        print(e)
        
def safety(bot, update):
    try:              
        update.message.reply_text("Safety Facts: \n1.Clean your hands often. Use soap and water, or an alcohol-based hand rub. \n2.Maintain a safe distance from anyone who is coughing or sneezing. \n3.Don\u2019t touch your eyes, nose or mouth. \n4.Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze. \n5.Stay home if you feel unwell. \n6.If you have a fever, a cough, and difficulty breathing, seek medical attention. Call in advance. \n7.Follow the directions of your local health authority.")
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return 
    except Exception as e:
        print(e)

def containmentzone(bot, update):
    try:
        print("bye")
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        loc = update.message.location
        global user_lat
        user_lat = loc.latitude
        global user_long
        user_long = loc.longitude
        print(user_lat)
        contents = requests.post('https://data.geoiq.io/dataapis/v1.0/covid/locationcheck',json={'key':"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtYWlsSWRlbnRpdHkiOiJjaGF2YW5zYW5pa2F2aWthc0BnbWFpbC5jb20ifQ.9GhEC_MyTUHxiB7hWQ1HowI7QjrRuiD_yaO8cEUl008",'latlngs':[[user_lat,user_long]]}).json()
        url = contents['data'][0]['inContainmentZone']
        print(url)
        if url == True:
            text = "Unfortunately, your location falls under the containment region. "+"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
        else:
            text = "Congratulations, your location doesnt fall under the containment region." +"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
        update.message.reply_text(text)
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return SET_STAT
    except Exception as e:
        print(e)
        update.message.reply_text("Service Timed Out. Please press start to continue.")

def containmentzoneR(bot, update):
    try:
        print("bye")
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        #loc = update.message.location
        contents = requests.post('https://data.geoiq.io/dataapis/v1.0/covid/locationcheck',json={'key':"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtYWlsSWRlbnRpdHkiOiJjaGF2YW5zYW5pa2F2aWthc0BnbWFpbC5jb20ifQ.9GhEC_MyTUHxiB7hWQ1HowI7QjrRuiD_yaO8cEUl008",'latlngs':[[user_lat,user_long]]}).json()
        url = contents['data'][0]['inContainmentZone']
        print(url)
        if url == True:
            text = "Unfortunately, your location falls under the containment region. "+"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
        else:
            text = "Congratulations, your location doesnt fall under the containment region." +"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
        update.message.reply_text(text)
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return 
    except Exception as e:
        print(e)    
        update.message.reply_text("Service Timed Out. Please press start to continue.")

def testingcenters(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        lstF = []
        loc = update.message.location
        global user_lat
        user_lat = loc.latitude
        global user_long
        user_long = loc.longitude
        locTup = (user_lat,user_long)
        worksheet = pd.read_csv('testcenter.csv')
        types = worksheet['Type'].tolist()
        hospitals = worksheet['Hospital'].tolist()
        latitude = worksheet['Latitude'].tolist()
        longitude = worksheet['Longitude'].tolist()
        for (a, b, c, d) in zip(types, hospitals, latitude, longitude):
            hospTup = (c,d)
            dist = geodesic(locTup, hospTup).miles
            finalTup = (a,b,dist)
            lstF.append(finalTup)
        sLst = sorted(lstF,key = lambda x: x[2])
        update.message.reply_text("The 5 closest testing centers to your location are:")
        for i in range(1,6):
            update.message.reply_text(str(i)+". "+sLst[i][1]+" Type: "+sLst[i][0])
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return SET_STAT
    except Exception as e:
        print(e)
        update.message.reply_text("Service Timed Out. Please press start to continue.")

def testingcentersR(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        lstF = []
        loc = update.message.location
        global user_lat
        #user_lat = loc.latitude
        global user_long
        #user_long = loc.longitude
        locTup = (user_lat,user_long)
        worksheet = pd.read_csv('testcenter.csv')
        types = worksheet['Type'].tolist()
        hospitals = worksheet['Hospital'].tolist()
        latitude = worksheet['Latitude'].tolist()
        longitude = worksheet['Longitude'].tolist()
        for (a, b, c, d) in zip(types, hospitals, latitude, longitude):
            hospTup = (c,d)
            dist = geodesic(locTup, hospTup).miles
            finalTup = (a,b,dist)
            lstF.append(finalTup)
        sLst = sorted(lstF,key = lambda x: x[2])
        update.message.reply_text("The 5 closest testing centers to your location are:")
        for i in range(1,6):
            update.message.reply_text(str(i)+". "+sLst[i][1]+" Type: "+sLst[i][0])
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return
    except Exception as e:
        print(e)
        update.message.reply_text("Service Timed Out. Please press start to continue.")

def menu(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        keyboard = [['Containment Zone', 'Testing Centers'],['Symptoms','Safety Measures'],['Live Updates','Helpline Number'],['Immunity Boosters','Myth Busters']]

        reply_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True,resize_keyboard=True)
        update.message.reply_text("Select an option to continue.", reply_markup=reply_markup)
    except Exception as e:
        print(e)
    
def servicetype(bot, update):
    try:
        global STATE
        TYPE = update.message.text
        print(TYPE)
        print(update.message.text)
        if update.message.text == 'Containment Zone':
            if user_lat == 0:
                STATE = CONTAINMENTZONE
                request_location(bot,update)
                return CONTAINMENTZONE
            else:
                STATE = CONTAINMENTZONER
                containmentzoneR(bot,update)
                return SET_STAT
        elif update.message.text == 'Testing Centers':
            print('t')
            if user_lat == 0:
                STATE = TESTINGCENTERS
                request_location(bot,update)
                return TESTINGCENTERS
            else:
                testingcentersR(bot,update)
                return SET_STAT
        elif update.message.text == 'Symptoms':
            print('sy')
            symptoms(bot, update)
            return SET_STAT
        elif update.message.text == 'Safety Measures':
            print('sf')
            STATE = SAFETY
            safety(bot, update)
            return SET_STAT
        elif update.message.text == 'Live Updates':
            print('l')
            print(user_lat)
            if user_lat == 0:
                STATE = LIVE_UPDATES
                request_location(bot,update)
                return LIVE_UPDATES
            else:
                live_updatesR(bot,update)
                return SET_STAT
        elif update.message.text == 'Myth Busters':
            print('sy')
            myth_buster(bot,update)
            return SET_STAT
        elif update.message.text == 'Immunity Boosters':
            print('sy')
            immunity_boost(bot,update)
            return SET_STAT
        elif update.message.text == 'Helpline Number':
            print('l')
            if user_lat == 0:
                STATE = HELPLINE_NUMBER
                request_location(bot,update)
                return HELPLINE_NUMBER
            else:
                helplinenumberR(bot,update)
                return SET_STAT
        elif update.message.text == 'Thanks':
            print("Finally")
            thanks(bot,update)
            return SET_STAT
        elif update.message.text == 'Menu':
            print("m")
            STATE = MENU
            menu(bot,update)
            return SET_STAT
        else:
            STATE = MENU
            return MENU
    except Exception as e:
        print(e)
        update.message.reply_text("Service Timed Out. Please press start to continue.")
        
def request_location(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        update.message.reply_text("Please attach your location from the Attachment option.",reply_markup=ReplyKeyboardRemove())
        return
    except Exception as e:
        print(e)
        
def start(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        global user_lat
        global user_long
        user_lat = 0
        user_long = 0
        keyboard = [['Containment Zone', 'Testing Centers'],['Symptoms','Safety Measures'],['Live Updates','Helpline Number'],['Immunity Boosters','Myth Busters']]
        text = "Hello "+update["message"]["chat"]["first_name"].capitalize()+"! My Name is CovidCare Bot. I can help you by providing various details you need to know about corona virus,like, \n 1. Check if your home is located within a containment area, and also check what colour zone your place of residence falls under.\n 2. Locate testing centres close to your home. \n 3. Check Live updates of Cases, Recovery and Fatality rate across the country, your state and your district. \n 4. Get information about the government issued helplines for Covid - 19 for your state as well as for the country. \n 5. Obtain information about the various Ayurvedic and Home remedies that can boost your immunity. \n 6. Be aware of various myths that have been spreading around the world. \n 7. Know what safety measures to be followed. \n 8. Also know what symptoms are to be paid attention to. \n\n Select an option to continue."
        update.message.reply_text(text,reply_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True,resize_keyboard=True))
        return SET_STAT
    except Exception as e:
        print(e) 
    
def thanks(bot, update):
    try:
        global user_lat
        user_lat = 0
        global user_long
        user_long = 0
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        text = "You're Welcome "+update["message"]["chat"]["first_name"].capitalize()+"! Stay Home, Stay Safe!"
        update.message.reply_text(text)
    except Exception as e:
        print(e)
        
def echo(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        text = "Please attach your location from the Attachment option or /cancel to cancel this action."
        update.message.reply_text(text,reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        print(e)    

def cancel(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        text = "User Cancelled this action."
        update.message.reply_text(text)
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],one_time_keyboard=True,resize_keyboard=True))
        return SET_STAT
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
            SET_STAT: [RegexHandler('^(Containment Zone|Testing Centers|Symptoms|Safety Measures|Live Updates|Helpline Number|Immunity Boosters|Myth Busters|Thanks|Menu)$',servicetype)],
            MENU: [MessageHandler(Filters.text, menu)],
            CONTAINMENTZONE: [MessageHandler(Filters.location, containmentzone),CommandHandler('cancel', cancel),MessageHandler(Filters.text, echo)],
            LIVE_UPDATES: [MessageHandler(Filters.location, live_updates),CommandHandler('cancel', cancel),MessageHandler(Filters.text, echo)],
            TESTINGCENTERS: [MessageHandler(Filters.location, testingcenters),CommandHandler('cancel', cancel),MessageHandler(Filters.text, echo)],
            HELPLINE_NUMBER: [MessageHandler(Filters.location, helplinenumber),CommandHandler('cancel', cancel),MessageHandler(Filters.text, echo)]
             },
        fallbacks=[CommandHandler('start', start),CommandHandler('cancel', cancel),MessageHandler(Filters.text, menu)]
    )

    dp.add_handler(conv_handler)
    #updater.start_polling()
    #updater.idle()
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
    updater.bot.setWebhook('https://quiet-escarpment-71463.herokuapp.com/' + TOKEN)

if __name__ == '__main__':
    main()

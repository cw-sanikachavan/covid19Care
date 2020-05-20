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
LIVE_UPDATES, MENU, SET_STAT, CONTAINMENTZONE, TESTINGCENTERS, HELPLINE_NUMBER, SYMPTOMS, SAFETY = range(8)
STATE = SET_STAT
def helplinenumber(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        lstF = []
        loc = update.message.location
        user_lat = loc.latitude
        user_long = loc.longitude
        locTup = (user_lat,user_long)
        worksheet = pd.read_csv('https://raw.githubusercontent.com/sanikachavan/covid19Care/master/coronvavirushelplinenumber.csv',sep=",")
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
                update.message.reply_text("Type /thanks if done or /menu to select another option.")
    except Exception as e:
        print(e)

def immunity_boost(bot,update):
    bot.send_photo(chat_id=update.message.chat.id, photo="https://www.ayush.gov.in/img/m2.jpeg")
    bot.send_photo(chat_id=update.message.chat.id, photo="https://www.ayush.gov.in/img/m3.jpeg")
    bot.send_photo(chat_id=update.message.chat.id, photo="https://www.ayush.gov.in/img/m4.jpeg")
    update.message.reply_text("Source: https://www.ayush.gov.in/")
    update.message.reply_text("Type /thanks if done or /menu to select another option.")
    
def myth_buster(bot,update):
    bot.send_photo(chat_id=update.message.chat.id, photo="https://english.cdn.zeenews.com/sites/default/files/2020/03/28/851333-m-t-10.gif")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://english.cdn.zeenews.com/sites/default/files/2020/03/28/851332-m-t-9.gif")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://english.cdn.zeenews.com/sites/default/files/2020/03/28/851331-m-t-8.gif")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://english.cdn.zeenews.com/sites/default/files/2020/03/28/851330-m-t-7.gif")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://english.cdn.zeenews.com/sites/default/files/2020/03/28/851329-m-t-6.gif")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://english.cdn.zeenews.com/sites/default/files/2020/03/28/851328-m-t-5.gif")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://english.cdn.zeenews.com/sites/default/files/2020/03/28/851327-m-t-4.gif")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://english.cdn.zeenews.com/sites/default/files/2020/03/28/851326-m-t-3.gif")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://english.cdn.zeenews.com/sites/default/files/2020/03/28/851325-m-t-2.gif")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://english.cdn.zeenews.com/sites/default/files/2020/03/28/851324-m-t-1.gif")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://pbs.twimg.com/media/EUWmOL5UEAAWbWC.jpg")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/90982752_2869333156514188_7422268176903176192_o.jpg?_nc_cat=105&_nc_sid=cdbe9c&_nc_ohc=DxidHjLpZb4AX8AR4Lt&_nc_ht=scontent.fbom19-1.fna&oh=ca448b149167c866eb3b79c55103bc60&oe=5EEC4654")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-2.fna.fbcdn.net/v/t1.0-9/91221243_2869333573180813_7233028666551173120_o.jpg?_nc_cat=100&_nc_sid=cdbe9c&_nc_ohc=FMdlyHH-rV8AX87iX5Y&_nc_ht=scontent.fbom19-2.fna&oh=15d540e6b35fad5e9a38433b7662ec14&oe=5EE9D469")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/91380693_2872401962873974_7980933818842349568_o.jpg?_nc_cat=105&_nc_sid=cdbe9c&_nc_ohc=XtKQsCE1aJ4AX-Whh_4&_nc_ht=scontent.fbom19-1.fna&oh=831bfe980c9b643a79145b3868dd5533&oe=5EEA3B02")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-2.fna.fbcdn.net/v/t1.0-9/91321758_2872402052873965_1440716358189842432_o.jpg?_nc_cat=100&_nc_sid=cdbe9c&_nc_ohc=MfzPny9zBqAAX8hhI42&_nc_ht=scontent.fbom19-2.fna&oh=a4cb51be8b4fe961f4ade42cb4a721a7&oe=5EEB98FC")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/91358488_2872402136207290_5425936488317583360_o.jpg?_nc_cat=109&_nc_sid=cdbe9c&_nc_ohc=Vpmv4wJ4BJUAX_j7pj6&_nc_ht=scontent.fbom19-1.fna&oh=78a1dde2f9aad58227029949ed096859&oe=5EEB6BE4")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/92098854_2872402206207283_9096256621394264064_o.jpg?_nc_cat=101&_nc_sid=cdbe9c&_nc_ohc=JmAKdbVX4IoAX8FwtX3&_nc_ht=scontent.fbom19-1.fna&oh=b53a8355a0020883ec16a919e028c7ff&oe=5EE96C8E")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/91876882_2876219299158907_7455677645167001600_o.jpg?_nc_cat=105&_nc_sid=cdbe9c&_nc_ohc=eeseMm54GdgAX_6natE&_nc_ht=scontent.fbom19-1.fna&oh=4f6171e4ca4804a2b93e97014c2fa5b8&oe=5EE96BEF")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/91898377_2876219272492243_8098992655809118208_o.jpg?_nc_cat=105&_nc_sid=cdbe9c&_nc_ohc=ktST61DLu1sAX_Pheh9&_nc_ht=scontent.fbom19-1.fna&oh=d3444355aaa684247384fe75a00e21c0&oe=5EEAE380")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/91420473_2876219312492239_2296966303950307328_o.jpg?_nc_cat=107&_nc_sid=cdbe9c&_nc_ohc=NpJzz2RYjqEAX8DVj4Q&_nc_ht=scontent.fbom19-1.fna&oh=bb696bd9eb12669631eaca3f180c7507&oe=5EE99F3F")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/91703210_2876219439158893_6135084083362922496_o.jpg?_nc_cat=105&_nc_sid=cdbe9c&_nc_ohc=peYNmz0z3CoAX-E2rCX&_nc_ht=scontent.fbom19-1.fna&oh=e7321d77b202826259ea214da98bf03f&oe=5EEC5873")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/92795217_2886359531478217_3220302938794622976_o.jpg?_nc_cat=109&_nc_sid=cdbe9c&_nc_ohc=-rgXdhvzW_8AX-InkeJ&_nc_ht=scontent.fbom19-1.fna&oh=82c80114da72170abede28d04d235b26&oe=5EE96F71")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-2.fna.fbcdn.net/v/t1.0-9/92572155_2886359508144886_2371728722362368000_o.jpg?_nc_cat=106&_nc_sid=cdbe9c&_nc_ohc=Ar3123AvPkIAX8ovcXO&_nc_ht=scontent.fbom19-2.fna&oh=86f9e848aecdf391b7dc1ad67049376a&oe=5EEB319B")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-2.fna.fbcdn.net/v/t1.0-9/92516837_2891273190986851_2180450717452468224_o.jpg?_nc_cat=106&_nc_sid=cdbe9c&_nc_ohc=8noxnL21GVEAX_yQOyG&_nc_ht=scontent.fbom19-2.fna&oh=b714e8f4af6a41b6f91c7c95be36c656&oe=5EEA15D5")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-2.fna.fbcdn.net/v/t1.0-9/92579544_2891273197653517_4819304316609232896_o.jpg?_nc_cat=111&_nc_sid=cdbe9c&_nc_ohc=d1kR9eUE4vYAX-NkZcu&_nc_ht=scontent.fbom19-2.fna&oh=657d3df8c5abe2b57ae574cbe8930718&oe=5EEC42AC")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/92021249_2891273180986852_3821770618487963648_o.jpg?_nc_cat=102&_nc_sid=cdbe9c&_nc_ohc=-9Wnz6371QgAX_I3ZkM&_nc_ht=scontent.fbom19-1.fna&oh=ee3f9f59513b5fa22b126e9623421101&oe=5EEB9667")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/92907913_2891273320986838_8661860489455730688_o.jpg?_nc_cat=102&_nc_sid=cdbe9c&_nc_ohc=I0sRnvz3xl4AX_2eVBv&_nc_ht=scontent.fbom19-1.fna&oh=f15348eee4d8526db545e4d4c787d1fd&oe=5EEC087E")
    time.sleep(5)
    bot.send_photo(chat_id=update.message.chat.id, photo="https://scontent.fbom19-1.fna.fbcdn.net/v/t1.0-9/92459150_2895852420528928_4494651578405355520_o.jpg?_nc_cat=101&_nc_sid=cdbe9c&_nc_ohc=UfZtRwWcGI8AX_Rmq8s&_nc_ht=scontent.fbom19-1.fna&oh=00599adcfe670fc7fba6f7054b4c4296&oe=5EEBE622")
    update.message.reply_text("Source: MyGov Corona Hub FB Page")
    update.message.reply_text("Type /thanks if done or /menu to select another option.")
    
def live_updates(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        covid = Covid()
        data = covid.get_status_by_country_name("india")
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
        print(district,state)
        if district == "Mumbai Suburban":
            district = "Mumbai"
        print(district,state)
        js = requests.get("https://api.covid19india.org/v2/state_district_wise.json").json()
        for i in js:
            if state == i['state']:
                for j in i['districtData']:
                    stateA = stateA + j['active']
                    stateR = stateR + j['recovered']
                    stateC= stateC + j['confirmed']
                    stateD = stateD + j['deceased']
                    if j['district'] == district:
                        text = "Total Confirmed cases in "+district+" are: "+str(j['confirmed'])+"\nTotal Active cases in "+district+" are: "+ str(j['active'])+"\nTotal Recovered cases in "+district+" are: "+ str(j['recovered'])+"\nTotal Deceased cases in "+district+" are: "+ str(j['deceased'])+"\nRecovery Rate in "+district+":"+str(round(j['recovered']/j['confirmed'],2))+"\nMortality Rate in "+district+":"+str(round(j['deceased']/j['confirmed'],2))
                        print(str(j['confirmed']))
                        print(j['recovered']/j['confirmed'])
        print(stateA)
<<<<<<< HEAD
        update.message.reply_text("Total Confirmed cases in India are: "+str(data['confirmed'])+"\nTotal Active cases in India are: "+ str(data['active'])+"\nTotal Recovered cases in India are: "+ str(data['recovered'])+"\nTotal Deceased cases in India are: "+ str(data['deaths']))+"\nRecovery Rate in India:"+str(round(data['recovered']/data['confirmed'],2))+"\nMortality Rate in India:"+str(round(data['deaths']/data['confirmed'],2)))
        update.message.reply_text("Total Confirmed cases in "+state+" are: "+str(stateC)+"\nTotal Active cases in "+state+" are: "+ str(stateA)+"\nTotal Recovered cases in "+state+" are: "+ str(stateR)+"\nTotal Deceased cases in "+state+" are: "+ str(stateD))+"\nRecovery Rate in "+state+":"+str(round(stateR/stateC,2))+"\nMortality Rate in "+state+":"+str(round(stateD/stateC,2)))
=======
        update.message.reply_text("Total Confirmed cases in India are: "+str(data['confirmed'])+"\nTotal Active cases in India are: "+ str(data['active'])+"\nTotal Recovered cases in India are: "+ str(data['recovered'])+"\nTotal Deceased cases in India are: "+ str(data['deaths'])+"\nRecovery Rate in India:"+str(round(data['recovered']/data['confirmed'],2))+"\nMortality Rate in India:"+str(round(data['deaths']/data['confirmed'],2)))
        update.message.reply_text("Total Confirmed cases in "+state+" are: "+str(stateC)+"\nTotal Active cases in "+state+" are: "+ str(stateA)+"\nTotal Recovered cases in "+state+" are: "+ str(stateR)+"\nTotal Deceased cases in "+state+" are: "+ str(stateD)+"\nRecovery Rate in "+state+":"+str(round(stateR/stateC,2))+"\nMortality Rate in "+state+":"+str(round(stateD/stateC,2)))
>>>>>>> 86ab0ac454fdc6132320b52f94ef37ba5557e1f4
        update.message.reply_text(text)
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
        worksheet = pd.read_csv('https://raw.githubusercontent.com/sanikachavan/covid19Care/master/testcenter.csv',sep=",")
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
        update.message.reply_text("Type /thanks if done or /menu to select another option.")
    except Exception as e:
        print(e)


def helplinenumber(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        lstF = []
        loc = update.message.location
        user_lat = loc.latitude
        user_long = loc.longitude
        locTup = (user_lat,user_long)
        worksheet = pd.read_csv('https://raw.githubusercontent.com/sanikachavan/covid19Care/master/coronvavirushelplinenumber.csv',sep=",")
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
                update.message.reply_text("Type /thanks if done or /menu to select another option.")
    except Exception as e:
        print(e)
        
        

def menu(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
<<<<<<< HEAD
        keyboard = [['Containment_Zone'], ['Testing_Centers'],['Symptoms'],['Safety_Measures'],['Live_Updates'],['Helpline_Number'],['Immunity_Boosters'],['Myth_Busters']]

=======
        keyboard = [['Containment_Zone'], ['Testing_Centers'],['Symptoms'],['Safety_Measures'],['Live_Updates'],['Helpline_Number']]
>>>>>>> 86ab0ac454fdc6132320b52f94ef37ba5557e1f4
        reply_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True,resize_keyboard=True)
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
            request_location(bot,update)
            return LIVE_UPDATES
<<<<<<< HEAD
        elif update.message.text == 'Myth_Busters':
            print('sy')
            myth_buster(bot,update)
            return MENU
        elif update.message.text == 'Immunity_Boosters':
            print('sy')
            immunity_boost(bot,update)
            return MENU
=======
>>>>>>> 86ab0ac454fdc6132320b52f94ef37ba5557e1f4
        elif update.message.text == 'Helpline_Number':
            print('l')
            STATE = HELPLINE_NUMBER
            request_location(bot,update)
            return HELPLINE_NUMBER
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
<<<<<<< HEAD
        keyboard = [['Containment_Zone'], ['Testing_Centers'],['Symptoms'],['Safety_Measures'],['Live_Updates'],['Helpline_Number'],['Immunity_Boosters'],['Myth_Busters']]
=======
        keyboard = [['Containment_Zone'], ['Testing_Centers'],['Symptoms'],['Safety_Measures'],['Live_Updates'],['Helpline_Number']]
>>>>>>> 86ab0ac454fdc6132320b52f94ef37ba5557e1f4
        text = "Hello "+update["message"]["chat"]["first_name"].capitalize()+"! My Name is CovidCare Bot. I can help you by letting you by providing various details you need to know about corona virus. Select an option to continue."
        update.message.reply_text(text,reply_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True,resize_keyboard=True))
        return SET_STAT
    except Exception as e:
        print(e) 
    
def thanks(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        text = "You're Welcome "+update["message"]["chat"]["first_name"].capitalize()+"! Stay Home, Stay Safe!"
        update.message.reply_text(text)
    except Exception as e:
        print(e) 
def echo(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        text = "I'm sorry, I'm afraid I can't provide information for this."
        update.message.reply_text(text)
    except Exception as e:
        print(e)    

def main():
    updater = Updater(t)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
<<<<<<< HEAD
            SET_STAT: [RegexHandler('^(Containment_Zone|Testing_Centers|Symptoms|Safety_Measures|Live_Updates|Helpline_Number|Immunity_Boosters|Myth_Busters)$',servicetype )],
=======
            SET_STAT: [RegexHandler('^(Containment_Zone|Testing_Centers|Symptoms|Safety_Measures|Live_Updates|Helpline_Number)$',servicetype )],
>>>>>>> 86ab0ac454fdc6132320b52f94ef37ba5557e1f4
            MENU: [CommandHandler('menu', menu)],
            CONTAINMENTZONE: [MessageHandler(Filters.location, containmentzone)],
            LIVE_UPDATES: [MessageHandler(Filters.location, live_updates)],
            TESTINGCENTERS: [MessageHandler(Filters.location, testingcenters)],
            HELPLINE_NUMBER: [MessageHandler(Filters.location, helplinenumber)]
             },
        fallbacks=[CommandHandler('start', start),CommandHandler('menu', menu),CommandHandler('thanks', thanks)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
    #updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
    #updater.bot.setWebhook('https://quiet-escarpment-71463.herokuapp.com/' + TOKEN)
if __name__ == '__main__':
    main()

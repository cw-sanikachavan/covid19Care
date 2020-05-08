from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
import json
import time
import os

TOKEN = "1156469077:AAGZvfC8XwNm7nqFUBvBhw6n2gYq1nb4WC4"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
    
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    
def echo_all(updates):
    for update in updates["result"]:
        try:
            chat = update["message"]["chat"]["id"]
            if "location" in update["message"]:
                loc = update["message"]["location"]

                if loc:
                    contents = requests.post('https://data.geoiq.io/dataapis/v1.0/covid/locationcheck',json={'key':"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtYWlsSWRlbnRpdHkiOiJjaGF2YW5zYW5pa2F2aWthc0BnbWFpbC5jb20ifQ.9GhEC_MyTUHxiB7hWQ1HowI7QjrRuiD_yaO8cEUl008",'latlngs':[[loc['latitude'],loc['longitude']]]}).json()
                    url = contents['data'][0]['inContainmentZone']
                    print(url)
                    if url == True:
                        text = "Unfortunately, your location falls under the containment region. "+"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
                    else:
                        text = "Congratulations, your location doesnt fall under the containment region." +"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
                    send_message(text, chat)
            if "text" in update["message"]:
                text = update["message"]["text"]
                if text == "/containmentzone":
                    send_message("Please send your location.",chat)
                elif text == "/locationcheck":
                    contents = requests.post('https://data.geoiq.io/dataapis/v1.0/covid/locationcheck',json={'key':"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtYWlsSWRlbnRpdHkiOiJjaGF2YW5zYW5pa2F2aWthc0BnbWFpbC5jb20ifQ.9GhEC_MyTUHxiB7hWQ1HowI7QjrRuiD_yaO8cEUl008",'latlngs':[[loc['latitude'],loc['longitude']]]}).json()
                    url = contents['data'][0]['inContainmentZone']
                    print(url)
                    if url == True:
                        text = "Unfortunately, your location falls under the containment region. "+"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
                    else:
                        text = "Congratulations, your location doesnt fall under the containment region." +"It lies in the "+contents['data'][0]['districtZoneType']+"."+" Stay Home, Stay Safe"
                    send_message(text, chat)
                    send_message("Type /thanks if done.",chat)
                elif text == "/start":
                    text = "Hello "+update["message"]["chat"]["first_name"].capitalize()+"! My Name is CovidCare Bot. I can help you by letting you know if your location falls under a containment zone. Type /containmentzone to know."
                    send_message(text, chat)
                elif text == "/thanks":
                    text = "You're Welcome "+update["message"]["chat"]["first_name"].capitalize()+"! Carry On."
                    send_message(text, chat)
                else:
                    text = "I'm sorry, I'm afraid I can't provide information for this."
                    send_message(text, chat)
        except Exception as e:
            print(e)    

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)
    
if __name__ == '__main__':
    main()

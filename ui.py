from google_client import *
from config import TOKEN
import telegram
from flask import Flask, Response, request
import json
from database_funcs import get_data_for_buttons


app = Flask(__name__)


def set_hotel_button(hotel_name):
    return [telegram.InlineKeyboardButton(hotel_name, callback_data=hotel_name)]


def get_next_activity(activity, activities):
    index = activities.index(activity)
    if index >= len(activities):
        return activity
    return activities[index + 1]


def get_previous_activity(activity, activities):
    index = activities.index(activity)
    if index == 0:
        return activity
    return activities[index - 1]


def set_activity_buttons(activity, hotel):
    return [
        telegram.InlineKeyboardButton('previous', callback_data='previous !' + activity + '!' + hotel),
        telegram.InlineKeyboardButton('next', callback_data='next !' + activity + '!' + hotel)
    ]


def show_only_hotels_buttons(chat_id, hotel_names):
    keyboard = [set_hotel_button(hotel_name) for hotel_name in hotel_names]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    print(reply_markup)
    temp = json.dumps(reply_markup.to_dict())
    print("temp: ", temp)
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                 .format(TOKEN, chat_id, "msg", temp))
    return Response("successful")


def show_first_activity(chat_id, message_id, data, chosen_hotel, activity):
    keyboard = []
    for hotel in data.keys():
        keyboard.append(set_hotel_button(hotel))
    keyboard.insert(0, set_activity_buttons(activity, chosen_hotel))
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    temp = json.dumps(reply_markup.to_dict())
    requests.get("https://api.telegram.org/bot{}/editMessageText?chat_id={}&message_id={}"
                 "&text={}&reply_markup={}"
                 .format(TOKEN, chat_id, message_id, activity + "\nHERE ACTIVITY DESCRIPTION", temp))
    return Response("success")

@app.route('/message', methods=["POST"])
def handle_message():
    #return Response('s')
    print("got message")
    print(request.get_json())
    if request.get_json().get('callback_query'):
        chat_id = request.get_json().get('callback_query').get('from').get('id')
        message_id = request.get_json().get('callback_query').get('message').get('message_id')
        callback_message = request.get_json().get('callback_query').get('data')
    else:
        chat_id = request.get_json()['message']['chat']['id']
        message_id = None
        callback_message = None

    data = get_data_for_buttons(chat_id)
    if callback_message:
        if callback_message.startswith('previous'):
            hotel = callback_message.split('!')[2]
            activity = get_previous_activity(callback_message.split('!')[1], data[hotel])
            return show_first_activity(chat_id, message_id, data, hotel, activity)
        if callback_message.startswith('next'):
            hotel = callback_message.split('!')[2]
            activity = get_next_activity(callback_message.split('!')[1], data[hotel])
            return show_first_activity(chat_id, message_id, data, hotel, activity)
        activity = data[callback_message][0]
        return show_first_activity(chat_id, message_id, data, callback_message, activity)
    return show_only_hotels_buttons(chat_id, data.keys())



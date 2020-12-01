from google_client import *
from config import TELEGRAM_INIT_WEBHOOK_URL, TOKEN
import telegram
from flask import Flask, Response, request
import json
from database_funcs import get_data_for_buttons

app = Flask(__name__)


def show_hotels():
    chat_id = request.get_json()['message']['chat']['id']
    mockdata = get_data_for_buttons(chat_id)
    print('chat_id ', chat_id)
    #keyboard = [[telegram.InlineKeyboardButton(temp, callback_data=temp) for
    #             temp in mockdata.keys()]]
    keyboard = [[telegram.InlineKeyboardButton(temp, callback_data=temp)] for
                 temp in mockdata.keys()]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    print(reply_markup)
    temp = json.dumps(reply_markup.to_dict())
    print("temp: ", temp)
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                 .format(TOKEN, chat_id, "msg", temp))
    return Response("successful")


def show_activities():
    chat_id = request.get_json().get('callback_query').get('from').get('id')
    #mockdata = get_data_for_buttons(chat_id)
    print("inside show activities")
    print("chat_idddddd ", chat_id)
    mockdata = get_data_for_buttons(chat_id)
    hotel = request.get_json().get('callback_query').get('data')
    print(hotel)
    activity = mockdata.get(hotel)[0]
    activities_keyboard = [
        [telegram.InlineKeyboardButton('previous', callback_data='previous !' + activity + '!' + hotel),
         telegram.InlineKeyboardButton('next', callback_data='next !' + activity + '!' + hotel)]]
    reply_markup = telegram.InlineKeyboardMarkup(activities_keyboard)
    temp = json.dumps(reply_markup.to_dict())
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}"
                 .format(TOKEN, chat_id, activity + "\nHERE ACTIVITY DESCRIPTION", temp))
    return Response("success")


def show_previous_activity():
    chat_id = request.get_json().get('callback_query').get('from').get('id')
    mockdata = get_data_for_buttons(chat_id)
    message_id = request.get_json().get('callback_query').get('message').get('message_id')
    current_activity = request.get_json().get('callback_query').get('data').split('!')[1]
    hotel = request.get_json().get('callback_query').get('data').split('!')[2]
    activities = mockdata.get(hotel)
    current_index = activities.index(current_activity)
    if current_index == 0:
        return Response("success")
    else:
        previous_activity = mockdata.get(hotel)[current_index - 1]
        activities_keyboard = [
            [telegram.InlineKeyboardButton('previous', callback_data='previous !' + previous_activity + '!' + hotel),
             telegram.InlineKeyboardButton('next', callback_data='next !' + previous_activity + '!' + hotel)]]
        reply_markup = telegram.InlineKeyboardMarkup(activities_keyboard)
        temp = json.dumps(reply_markup.to_dict())
        requests.get("https://api.telegram.org/bot{}/editMessageText?chat_id={}&message_id={}"
                     "&text={}&reply_markup={}"
                     .format(TOKEN, chat_id, message_id, previous_activity + "\nHERE ACTIVITY DESCRIPTION", temp))
        return Response("success")


def show_next_activity():
    chat_id = request.get_json().get('callback_query').get('from').get('id')
    mockdata = get_data_for_buttons(chat_id)
    message_id = request.get_json().get('callback_query').get('message').get('message_id')
    current_activity = request.get_json().get('callback_query').get('data').split('!')[1]
    hotel = request.get_json().get('callback_query').get('data').split('!')[2]
    print("data: ", request.get_json().get('callback_query').get('data'))
    print("hotel: ", hotel)
    activities = mockdata.get(hotel)
    current_index = activities.index(current_activity)
    if current_index == len(mockdata.get(hotel)) - 1:
        return Response("success")
    else:
        next_activity = mockdata.get(hotel)[current_index + 1]
        activities_keyboard = [
            [telegram.InlineKeyboardButton('previous',
                                           callback_data='previous !' + next_activity + '!' + hotel),
             telegram.InlineKeyboardButton('next', callback_data='next !' + next_activity + '!' + hotel)]]
        reply_markup = telegram.InlineKeyboardMarkup(activities_keyboard)
        temp = json.dumps(reply_markup.to_dict())
        requests.get("https://api.telegram.org/bot{}/editMessageText?chat_id={}&message_id={}"
                     "&text={}&reply_markup={}"
                     .format(TOKEN, chat_id, message_id, next_activity + "\nHERE ACTIVITY DESCRIPTION", temp))
        return Response("success")


def handle_message():
    # return Response('s')
    print("got message")
    print(request.get_json())
    if request.get_json().get('callback_query'):
        if request.get_json().get('callback_query').get('data').startswith('previous'):
            return show_previous_activity()
        if request.get_json().get('callback_query').get('data').startswith('next'):
            return show_next_activity()
        return show_activities()
    return show_hotels()





#@app.route('/message', methods=["POST"])
#def handle_message():
#    # return Response('s')
#    print("got message")
#    print(request.get_json())
#    if request.get_json().get('callback_query'):
#        if request.get_json().get('callback_query').get('data').startswith('previous'):
#            return show_previous_activity()
#        if request.get_json().get('callback_query').get('data').startswith('next'):
#            return show_next_activity()
#        return show_activities()
#    return show_hotels()


#if __name__ == '__main__':
#    app.run(port=5002, threaded=True)

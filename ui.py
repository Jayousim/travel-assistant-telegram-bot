from google_client import *
from config import TOKEN
import telegram
from flask import Flask, Response, request
import json
from database_funcs import *
from model import SearchEngine
giphy_api_key = '7zuDeZ3gqSF0rmJpkOai7b625nmYgOfO'

app = Flask(__name__)


def set_hotel_button(hotel_name):
    return [telegram.InlineKeyboardButton(hotel_name, callback_data=hotel_name)]


def get_next_activity(activity, activities):
    index = activities.index(activity)
    if index >= len(activities) - 1:
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


def show_only_hotels_buttons(chat_id, hotel_names, destination):
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                 .format(TOKEN, chat_id, "Yay!! Look what I found for you in " + destination))
    keyboard = [set_hotel_button(hotel_name) for hotel_name in hotel_names]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    print(reply_markup)
    temp = json.dumps(reply_markup.to_dict())
    print("temp: ", temp)
    gif = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={giphy_api_key}&q={destination + ' city'}&limit=1").json().get('data')[0].get('images').get('original').get('url')

    requests.get("https://api.telegram.org/bot{}/sendAnimation?chat_id={}&animation={}&reply_markup={}"
                 .format(TOKEN, chat_id, gif, temp))

    return Response("successful")


def show_first_activity(chat_id, message_id, data, chosen_hotel, activity):
    photo = get_photo_ref(activity)[0]
    print("photo ", photo)
    if not photo:
        photo = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
    else:
        photo = SearchEngine.get_place_photos_from_reference(photo)
    print("photo ", photo)
    keyboard = []
    for hotel in data.keys():
        keyboard.append(set_hotel_button(hotel))
    keyboard.insert(0, set_activity_buttons(activity, chosen_hotel))
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    telegram.Bot(TOKEN).editMessageMedia(chat_id, message_id,media=telegram.InputMediaPhoto(photo, caption=activity), reply_markup=reply_markup)
    return Response("success")

#@app.route('/message', methods=["POST"])
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

    data, destination = get_data_for_buttons(chat_id)
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
    return show_only_hotels_buttons(chat_id, data.keys(), destination)

if __name__ == '__main__':
    app.run(port=5002, threaded=True)

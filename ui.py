from google_client import *
from config import TOKEN
import telegram
from flask import Flask, Response, request
import json
from database_funcs import *
from model import SearchEngine
giphy_api_key = '7zuDeZ3gqSF0rmJpkOai7b625nmYgOfO'

app = Flask(__name__)

g_counter = 0
def set_hotel_button(hotel_name, length):
    global g_counter
    g_counter += 1
    return [telegram.InlineKeyboardButton(str(g_counter) + '. ' + hotel_name + ' - found ' + str(length), callback_data=hotel_name)]


def get_next_activity(activity, activities):
    if activities[0] == activities[-1]:
        return None
    index = activities.index(activity)
    if index >= len(activities) - 1:
        return activities[0]
        #return activity
    return activities[index + 1]


def get_previous_activity(activity, activities):
    if activities[0] == activities[-1]:
        return None
    index = activities.index(activity)
    if index == 0:
        return activities[-1]
        #return activity
    return activities[index - 1]


def set_activity_buttons(activity, hotel):
    return [
        telegram.InlineKeyboardButton('previous', callback_data='previous !' + activity + '!' + hotel),
        telegram.InlineKeyboardButton('next', callback_data='next !' + activity + '!' + hotel)
    ]


def show_only_hotels_buttons(chat_id, hotel_names, destination):
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                 .format(TOKEN, chat_id, "Yay!! Look what I found for you in " + destination))
    keyboard = [set_hotel_button(hotel_name, len(hotel_names.get(hotel_name))) for hotel_name in hotel_names.keys()]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    print(reply_markup)
    temp = json.dumps(reply_markup.to_dict())
    print("temp: ", temp)
    gif = requests.get(f"https://api.giphy.com/v1/gifs/search?api_key={giphy_api_key}&q={destination + ' city'}&limit=1").json().get('data')[0].get('images').get('original').get('url')

    requests.get("https://api.telegram.org/bot{}/sendAnimation?chat_id={}&animation={}&reply_markup={}"
                 .format(TOKEN, chat_id, gif, temp))

    return Response("successful")


def show_first_activity(chat_id, message_id, data, chosen_hotel, activity):
    print("activityyyyyyyyyyyyyy: ", activity)
    photo = get_photo_ref(activity)[0]
    print("photo ", photo)
    if photo == 'None':
        photo = 'https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg'
    else:
        photo = SearchEngine.get_place_photos_from_reference(photo).url
    print("photo ", photo)
    keyboard = []
    for hotel in data.keys():
        keyboard.append(set_hotel_button(hotel, len(data.get(hotel))))
    keyboard.insert(0, set_activity_buttons(activity, chosen_hotel))
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    telegram.Bot(TOKEN).editMessageMedia(chat_id, message_id,media=telegram.InputMediaPhoto(photo, caption=activity), reply_markup=reply_markup)
    return Response("success")

#@app.route('/message', methods=["POST"])
def handle_message():
    #return Response('s')
    global g_counter
    g_counter = 0
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
            if not activity:
                return Response('success')
            return show_first_activity(chat_id, message_id, data, hotel, activity)
        if callback_message.startswith('next'):
            hotel = callback_message.split('!')[2]
            activity = get_next_activity(callback_message.split('!')[1], data[hotel])
            if not activity:
                return Response('success')
            return show_first_activity(chat_id, message_id, data, hotel, activity)
        activity = data[callback_message][0]
        return show_first_activity(chat_id, message_id, data, callback_message, activity)
    return show_only_hotels_buttons(chat_id, data, destination)


if __name__ == '__main__':
    app.run(port=5002, threaded=True)


from dataclasses import dataclass
from database import *
from config import TOKEN
import requests
import emoji


from model import SearchEngine
send_message_req = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN)
send_photo_req = "https://api.telegram.org/bot{}/sendPhoto".format(TOKEN)


@dataclass
class Bot:
    engine = SearchEngine()
    last_hotels = []

    @staticmethod
    def send_message(chat_id, response):
        res = requests.get(send_message_req + "?chat_id={}&text={}"
                           .format(chat_id, response))

    @staticmethod
    def send_photo(chat_id, response):
        res = requests.get(send_photo_req + "?chat_id={}&text={}"
                           .format(chat_id, response))

    @staticmethod
    def greet_the_user(chat_id):
        response = f"{emoji.emojize(':waving_hand:')} welcome to travel assistance\n\n " \
                   f"provide me with your destination using the following format: 'travel to' <destination> "
        Bot.send_message(chat_id, response)
        return "success"

    @staticmethod
    def travel_destination(message, chat_id):
        my_list = message.split()
        insert_new_message(chat_id, my_list[2])
        if len(my_list) == 3:
            response = f"{my_list[2]}! great choice!! {emoji.emojize(':grinning_face_with_big_eyes:')}" \
                       f"\n\n now please specify your favorable attractions and activities " \
                       f"using the following format: 'category' <category>"
        else:
            response = "oops! you didn't specify a valid destination"
        Bot.send_message(chat_id, response)
        return "success"

    @staticmethod
    def category(message, chat_id):
        my_list = message.split()
        if len(my_list) == 2:
            category = my_list[1]
            destination = get_previous_message(chat_id)
            hotels = Bot.return_relevant_hotels(destination, category)
            response = f"yay we found some relevant hotels here what we found:\n {hotels}"
        else:
            response = "not a valid syntax"
        Bot.send_message(chat_id, response)
        return "success"

    @staticmethod
    def show_help_menu(message, chat_id):
        return Bot.send_message(chat_id, message)

    @staticmethod
    def get_photo_of_hotel(hotel_name):
        for hotel in Bot.last_hotels:
            if hotel.get('name') == hotel_name:
                return SearchEngine.get_place_photos(hotel)
      
    @staticmethod
    def return_relevant_hotels(destination, category):
        found_hotels, last_hotels = SearchEngine.find_top_stays_with_type(destination, category)
        response = ""
        for hotel, surrounding in found_hotels:
            response += hotel
            response += "which has "
            response += str(surrounding)
            response += " " + category
            response += " nearby"
            response += '\n'
        return response


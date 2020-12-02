from dataclasses import dataclass
from database_connection import *
from config import TOKEN
import requests
import emoji
from ui import handle_message

from model import SearchEngine
send_message_req = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN)

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
        image_url = requests.get(response)
        res = requests.get(send_message_req + "?chat_id={}&text={}".format(chat_id, image_url.url))

    @staticmethod
    def greet_the_user(chat_id):
        response = f"{emoji.emojize(':waving_hand:')} welcome! iam Trevo the travel assistant\n\n " \
                   f"provide me with your destination"
        Bot.send_message(chat_id, response)

    @staticmethod
    def travel_destination(message, chat_id):
        response = f"{message}! great choice!! {emoji.emojize(':grinning_face_with_big_eyes:')}" \
                   f"\n\n what would you like to be close by your hotel?\n" \

        Bot.send_message(chat_id, response)

    @staticmethod
    def category(message, chat_id):
        my_list = message.split()
        return handle_message()

    @staticmethod
    def get_hotel_images(message, chat_id):
        my_list = message.split()
        i = 2
        hotel_name = ""
        while i < len(my_list)-1:
            hotel_name += my_list[i]
            hotel_name += " "
            i += 1
        hotel_name += my_list[i]
        hotel_image_url = Bot.get_photo_of_hotel(hotel_name)
        Bot.send_photo(chat_id, hotel_image_url)
        return True


    @staticmethod
    def show_help_menu(message, chat_id):
        return Bot.send_message(chat_id, message)

    @staticmethod
    def get_photo_of_hotel(hotel_name):
        for hotel in Bot.last_hotels:
            if hotel.get('name') == hotel_name:
                return SearchEngine.get_place_photos(hotel)

    @classmethod
    def return_relevant_hotels(cls, destination, category):
        found_hotels, Bot.last_hotels = SearchEngine.find_top_stays_with_type(destination, category)
        response = ""
        for hotel, surrounding in found_hotels:
            response += hotel
            response += "which has "
            response += str(surrounding)
            response += " " + category
            response += " nearby"
            response += '\n'
        return response


from dataclasses import dataclass
from database import *
import emoji
from model import SearchEngine


@dataclass
class Bot:
    engine = SearchEngine()
    last_hotels = []

    @staticmethod
    def greet_the_user():
        return f"{emoji.emojize(':waving_hand:')} welcome to travel assistance\n\n " \
               f"provide me with your destination using the following format: 'travel to' <destination> "

    @staticmethod
    def travel_destination(message, chat_id):
        my_list = message.split()
        insert_new_message(chat_id, my_list[2])
        if len(my_list) == 3:
            return f"{my_list[2]}! great choice!! {emoji.emojize(':grinning_face_with_big_eyes:')}" \
                   f"\n\n now please specify your favorable attractions and activities " \
                   f"using the following format: 'category' <category>"
        else:
            return "oops! you didn't specify a valid destination"

    @staticmethod
    def category(message, chat_id):
        my_list = message.split()
        if len(my_list) == 2:
            category = my_list[1]
            destination = get_previous_message(chat_id)
            hotels = Bot.return_relevant_hotels(destination, category)

            return f"yay!! we found some relevant hotels here what we found:\n {hotels}\n\n" \
                   f"to see the hotel images use this format: 'show images' <hotel name>"
        else:
            return "not a valid syntax"

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
        hotel_images = Bot.get_photo_of_hotel(hotel_name)
        for image in hotel_images:
            return image

    @staticmethod
    def show_help_menu(message):
        return "func1"

    @staticmethod
    def get_photo_of_hotel(hotel_name):
        print(Bot.last_hotels)
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




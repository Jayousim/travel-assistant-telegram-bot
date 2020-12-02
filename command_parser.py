from travel_advisor_bot import Bot
from database_connection import *

commands = {
    'greet the user':       Bot.greet_the_user,
    'travel destination':   Bot.travel_destination,
    'category':             Bot.category,
    'help menu':            Bot.show_help_menu,
    'get images':           Bot.get_hotel_images
}


def parse_command(message, chat_id):
    divided_message = message.split()
    if "start" in divided_message[0]:
        insert_new_status(chat_id, 1)
        return commands['greet the user'](chat_id)
    status = get_status(chat_id)
    if status:
        if status[0][0] == 1 and len(divided_message) == 1:
            insert_new_status(chat_id, 2)
            return commands['travel destination'](divided_message[0], chat_id)
        elif status[0][0] == 2 and len(divided_message) == 1:
            insert_new_status(chat_id, 3)
            return commands['category'](message, chat_id)
        elif "help" in message:
            return commands['help menu'](message)
        elif "image" in message:
            return commands['get images'](message, chat_id)
    else:
        Bot.send_message(chat_id, "i didn't understand try again")

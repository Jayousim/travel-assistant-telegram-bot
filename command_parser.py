from travel_advisor_bot import Bot


commands = {
    'greet the user':       Bot.greet_the_user,
    'travel destination':   Bot.travel_destination,
    'category':             Bot.category,
    'help menu':            Bot.show_help_menu,
    'get images':           Bot.get_hotel_images
}


def parse_command(message, chat_id):
    if "start" in message:
        status =  1
        return commands['greet the user'](chat_id)
    elif "travel to" in message:
        return commands['travel destination'](message, chat_id)
    elif "category" in message:
        return commands['category'](message, chat_id)
    elif "help" in message:
        return commands['help menu'](message)
    elif "show images" in message:
        return commands['get images'](message, chat_id)
    else:
        Bot.send_message(chat_id, "i didn't understand try again")

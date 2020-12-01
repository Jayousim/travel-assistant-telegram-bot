from travel_advisor_bot import Bot


commands = {
    'greet the user':       Bot.greet_the_user,
    'travel destination':   Bot.travel_destination,
    'help menu':            Bot.show_help_menu
}


def parse_command(message):
    if "start" in message:
        return commands['greet the user']()
    if "travel to" in message:
        return commands['travel destination'](message)
    elif "help" in message:
        return commands['help menu'](message)
    return "I didn't understand try again"

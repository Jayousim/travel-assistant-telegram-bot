from dataclasses import dataclass
import emoji


@dataclass
class Bot:

    @staticmethod
    def greet_the_user():
        return f"{emoji.emojize(':waving_hand:')} welcome to travel assistance\n\n " \
               f"provide me with your destination using the following format: 'travel to' <destination> "

    @staticmethod
    def travel_destination(message):
        my_list = message.split()
        if len(my_list) == 3:
            return f"{my_list[2]}! great choice!! {emoji.emojize(':grinning_face_with_big_eyes:')}" \
                   f"\n\n now please specify your favorable attractions and activities " \
                   f"using the following format: 'category' <category>"
        else:
            return "oops! you didn't specify a valid destination"

    @staticmethod
    def travel_destination(message):
        my_list = message.split()
        if len(my_list) == 3:
            return f"{my_list[2]}! great choice!! {emoji.emojize(':grinning_face_with_big_eyes:')}" \
                   f"\n\n now please specify your favorable attractions and activities " \
                   f"using the following format: 'category' <category>"
        else:
            return "oops! you didn't specify a valid destination"

    @staticmethod
    def show_help_menu(message):
        return "func1"
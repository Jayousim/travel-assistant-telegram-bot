from google_client import GoogleApiInvoker
from database_funcs import insert_data

class SearchEngine:
    @staticmethod
    def find_top_stays_with_type(destination, activity_type):
        hotels = GoogleApiInvoker.get_hotels(destination)
        hotels_activities = []
        hotels_jsons_activities = []
        for hotel in hotels:
            hotels_activities.append(
                [hotel.get('name'), GoogleApiInvoker.get_activities_by_hotel(hotel, activity_type)])
            hotels_jsons_activities.append(
                [hotel, GoogleApiInvoker.get_activities_by_hotel(hotel, activity_type)])
        hotels_activities = sorted(hotels_activities, key=lambda item_: len(item_[1]), reverse=True)
        hotels_jsons_activities = sorted(hotels_jsons_activities, key=lambda item_: len(item_[1]), reverse=True)
        insert_data(hotels_activities[:GoogleApiInvoker.MAX_HOTELS], destination, activity_type)
        return [(temp[0], len(temp[1])) for temp in hotels_jsons_activities[:GoogleApiInvoker.MAX_HOTELS]]

    def get_more_hotels_neraby(self):
        pass


    @staticmethod
    # gets the url query of photos
    def get_place_photos(location):
        photos_info = location.get('photos')[0]
        return GoogleApiInvoker.get_place_photos(photos_info['photo_reference'])

    @staticmethod
    def get_place_photos_from_reference(reference):
        return GoogleApiInvoker.get_place_photos(reference)


    @staticmethod
    def get_street_photos(location):
        pass

    @staticmethod
    def get_place_description(place):
        pass

    @classmethod
    def get_website_by_place_id(cls, place_id):
        return GoogleApiInvoker.get_website_by_place_id(place_id)





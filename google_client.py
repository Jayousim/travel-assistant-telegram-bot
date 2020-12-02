import requests
from config import GOOGLE_KEY


class GoogleApiInvoker:
    key = GOOGLE_KEY
    textsearch = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    nearbysearch = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    photo_request = 'https://maps.googleapis.com/maps/api/place/photo?'
    radius = 100
    MAX_HOTELS = 5

    @staticmethod
    def get_place_photos(reference):
        photo_query = reference
        maxwidth = "maxwidth=400"
        maxheight = "maxheight=400"
        ans = requests.get(f"{GoogleApiInvoker.photo_request}{maxwidth}&{maxheight}&key={GoogleApiInvoker.key}&photoreference={photo_query}")
        return ans

    @staticmethod
    def get_street_photos(loacation):
        pass

    @staticmethod
    def get_place_description(place):
        pass

    @staticmethod
    def get_hotels(destination):
        hotels_query = f"hotels in {destination}"
        ans = requests.get(f"{GoogleApiInvoker.textsearch}key={GoogleApiInvoker.key}&query={hotels_query}").json()
        hotels = ans.get("results")
        #hotels += GoogleApiInvoker.get_next_hotels(ans.get('next_page_token'))
        return hotels

    @staticmethod
    def get_next_hotels(next_page):
        if not next_page:
            return []
        result = requests.get(f"{GoogleApiInvoker.textsearch}key={GoogleApiInvoker.key}"
                              f"&pagetoken={next_page}").json()
        return result.get("results") + GoogleApiInvoker.get_next_hotels(result.get('next_page_token'))

    @staticmethod
    def get_location_from_json(data):
        return data.get('geometry').get('location').get('lat'), data.get('geometry').get('location').get('lng')

    @staticmethod
    def get_next_activities(next_page):
        if not next_page:
            return []
        result = requests.get(f"{GoogleApiInvoker.nearbysearch}key={GoogleApiInvoker.key}"
                              f"&pagetoken={next_page}").json()
        return result.get("results") + GoogleApiInvoker.get_next_activities(result.get('next_page_token'))

    @staticmethod
    def get_activities_by_hotel(hotel, activity):
        lat, lng = GoogleApiInvoker.get_location_from_json(hotel)
        ans = requests.get(
            f"{GoogleApiInvoker.nearbysearch}key={GoogleApiInvoker.key}&location={lat},{lng}"
            f"&radius={GoogleApiInvoker.radius}&keyword={activity}").json()
        current_results = ans.get("results")
        #current_results += GoogleApiInvoker.get_next_activities(ans.get('next_page_token'))
        return [(item.get('name'),item.get('photos', [{'photo_reference':None}])[0].get('photo_reference')) for item in current_results]

    @staticmethod
    def get_website_by_place_id(place_id):
        place_details = requests.get(f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,formatted_phone_number,website&key={GOOGLE_KEY}").json()
        return place_details['result']['website']



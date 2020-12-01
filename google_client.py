import time
from flask import Flask, request
import requests
from config import GOOGLE_KEY


class GoogleApiInvoker:
    key = GOOGLE_KEY
    textsearch = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    nearbysearch = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    radius = 1000
    MAX_HOTELS = 5

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
        hotels += GoogleApiInvoker.get_next_hotels(ans.get('next_page_token'))
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
        while ans.get("next_page_token"):
            time.sleep(2)
            ans = requests.get(
                f"{GoogleApiInvoker.nearbysearch}key={GoogleApiInvoker.key}"
                f"&pagetoken={ans.get('next_page_token')}").json()
            current_results += ans.get("results")
        return [item.get('name') for item in current_results]

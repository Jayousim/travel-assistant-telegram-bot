import time
from flask import Flask,request
import requests
from config import GOOGLE_KEY


class GoogleApiInvoker:
    key = GOOGLE_KEY
    textsearch = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    nearbysearch = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    @staticmethod

    @staticmethod
    def get_street_photos(loacation):
        pass

    @staticmethod
    def get_place_description(place):
        pass

    @staticmethod
    def get_all_hotels(destination):
        hotels_query = f"hotels in {destination}"
        ans = requests.get(f"{GoogleApiInvoker.textsearch}key={GoogleApiInvoker.key}&query={hotels_query}").json()
        hotels = ans.get("results")
        while ans.get("next_page_token"):
            time.sleep(2)
            ans = requests.get(f"{GoogleApiInvoker.textsearch}key={GoogleApiInvoker.key}&pagetoken={ans.get('next_page_token')}").json()
            hotels += ans.get("results")
        return hotels

    @staticmethod
    def get_by_keyword(keyword):
        ans = requests.get(
            f"{nearbysearch}key={key}&location={hotel_lats[i]},{hotel_lngs[i]}&radius={radius}&keyword={keyword}").json()
        current_results = ans.get("results")
        while ans.get("next_page_token"):
            time.sleep(2)
            ans = requests.get(f"{nearbysearch}key={key}&pagetoken={ans.get('next_page_token')}").json()
            current_results += ans.get("results")
        return [item.get('name') for item in current_results]


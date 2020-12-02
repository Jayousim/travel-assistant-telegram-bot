from database_connection import DBConnection
from flask import request


def insert_data(hotels_activities, destination, activity_type):
    chat_id = request.get_json()['message']['chat']['id']
    print("id: ", chat_id)
    for item in hotels_activities:
        for activity in item[1]:
            with DBConnection.Instance().get_db().cursor() as cursor:
                query = f'INSERT INTO destinations (chat_id, destination, category, hotel_name, activity_name) ' \
                        f'VALUES ({chat_id}, "{destination[0][0]}", "{activity_type}", "{item[0]}", "{activity}")'
                cursor.execute(query)
                DBConnection.Instance().get_db().commit()

def get_data_for_buttons(chat_id):
    ans = {}
    with DBConnection.Instance().get_db().cursor() as cursor:
        print("chat_id ", chat_id)
        query = f'SELECT hotel_name, activity_name FROM destinations WHERE chat_id={chat_id}'
        cursor.execute(query)
        result = cursor.fetchall()
        for item in result:
            ans[item[0]] = []
        for item in result:
            ans[item[0]] += [item[1]]
    return ans


from flask import Flask, Response, request
from config import TOKEN
from command_parser import parse_command
import requests


app = Flask(__name__)


@app.route('/sanity')
def sanity():
    return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message" + " " + request.get_json()['message']['text'])
    chat_id = request.get_json()['message']['chat']['id']
    message = request.get_json()['message']['text']

    response = parse_command(message, chat_id)

    # res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
    #              .format(TOKEN, chat_id, response))

    return Response("success", 200)


if __name__ == '__main__':
    app.run(port=5002, threaded=True)












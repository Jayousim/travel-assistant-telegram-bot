from flask import Flask, Response, request
from config import TOKEN
from command_parser import parse_command
import requests
import ui


app = Flask(__name__)


@app.route('/sanity')
def sanity():
    return "Server is running"

@app.route('/message', methods=["POST"])
def handle_message():
    #return Response("ack")
    if request.get_json().get('callback_query'):
        ui.handle_message()
        return Response('success')
    print("got message" + " " + request.get_json()['message']['text'])
    chat_id = request.get_json()['message']['chat']['id']
    message = request.get_json()['message']['text']
    response = parse_command(message, chat_id)
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002, threaded=True)












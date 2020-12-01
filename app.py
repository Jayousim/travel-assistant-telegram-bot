from flask import Flask, Response, request
from config import TELEGRAM_INIT_WEBHOOK_URL, TOKEN
from parser import parse_command
import requests

app = Flask(__name__)


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    message = request.get_json()['message']['text']
    response = parse_command(message)

    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                 .format(TOKEN, chat_id, response))
    return Response("success")


if __name__ == '__main__':
    requests.get(TELEGRAM_INIT_WEBHOOK_URL)
    app.run(port=5002, threaded=True)











import requests

TOKEN = '1465334834:AAFTxfNe4rR0lxx0TQnsuvgZNZzCIowLB_E'
server_ip = 'https://76abed448dca.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, server_ip)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

GOOGLE_KEY = "AIzaSyBONgiulyX32tzphZd1Iti5VbfNpi5L_0k"
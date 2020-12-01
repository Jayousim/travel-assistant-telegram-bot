import requests

TOKEN = '1425368104:AAGxzBKjlsnTkHi_SsonNSMK7eL_dfuqLFs'
server_ip = 'https://6c383b5b420a.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, server_ip)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

GOOGLE_KEY = "AIzaSyBONgiulyX32tzphZd1Iti5VbfNpi5L_0k"
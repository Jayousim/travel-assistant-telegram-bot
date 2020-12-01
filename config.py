import requests

TOKEN = '1405624434:AAEW850Cijffs2gWSQvdzDmY_oBS2heBi68'
server_ip = 'https://a4b1749b1300.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, server_ip)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

GOOGLE_KEY = "AIzaSyBONgiulyX32tzphZd1Iti5VbfNpi5L_0k"





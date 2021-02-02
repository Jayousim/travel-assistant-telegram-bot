import requests

TOKEN = '1405624434:AAEW850Cijffs2gWSQvdzDmY_oBS2heBi68' ## enter bot-id here, id you get when creating new bot with telegram app
server_ip = 'https://222c9ff8ec05.ngrok.io'  ## enter here the server id you get with ngrok and the command ngrok http 3000 
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, server_ip)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

data_base_pass = '1234' ## data base server password here
GOOGLE_KEY = "AIzaSyBONgiulyX32tzphZd1Iti5VbfNpi5L_0k" ## google place api key, you can get free 3 months account 
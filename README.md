

# travil assistant bot that given city can suggests you places to stay according to you favorite activity

## you first have to have mysql and pytohn3 with flask, pymysql on your machine.
## then got and create bot in telegram. you find the instructions here : https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0

###you have to set-up the following in the config-file  :

#### 1- TOKEN bot-id. id you get when creating new bot with telegram app
#### 2- server_ip: enter here the server id. to use local server, you get with ngrok and the command ngrok http 3000.
#### 3- GOOGLE_KEY = google place api key, you can get free 3 months account 
#### 4- data_base_pass = password for database root account.

#### then run the config.py file a once. 
#### then a server.py. 
#### if you dont have public ip. you get with ngrok and the command ngrok http 3000. the port we run the local server on.
#### now, you got the server ready to serve the bot. 
#### open telegram on phone or pc. open your new chat bot, with the name you gave it

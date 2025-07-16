from flask import Flask, request
import requests

TOKEN = '7568109007:AAEIdBvdMobMZu2Mh7TRJ50_hZ6FFRp5C6c'
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '')
    if text == '/start':
        requests.post(URL, json={'chat_id': chat_id, 'text': "Ma'un бот фаол ишлаяпти! /add, /list, /search!"})
    return {'ok': True}

if __name__ == '__main__':
    app.run()

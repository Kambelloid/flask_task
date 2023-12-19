from flask import Flask, request
import requests
import os

app = Flask(__name__)

def send_message(chat_id, message_id, text):
    method = 'sendMessage'
    token = os.environ['TELEGRAM_TOKEN']
    url = f'https://api.telegram.org/bot{token}/{method}'
    data = {'chat_id': chat_id, 'reply_to_message_id': message_id, 'text': text}
    requests.post(url, data=data)
    
@app.route('/', methods=['GET', 'POST'])
def receive_update():
    if request.method == 'POST':
        print(request.json)
        chat_id = request.json['message']['chat']['id']
        message_id = request.json['message']['message_id']
        send_message(chat_id, message_id, 'pong')
    return {'ok': True}


if __name__ == "__main__":
    app.run()
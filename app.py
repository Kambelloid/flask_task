from flask import Flask, request
import requests
import os, json

app = Flask(__name__)

def send_message(chat_id, message_id):
    method = 'sendMessage'
    token = os.environ['TELEGRAM_TOKEN']
    weather_token = os.environ['WEATHER_TOKEN']
    url = f'https://api.telegram.org/bot{token}/{method}'
    
    weather = requests.get(f'http://api.weatherstack.com/current?access_key={weather_token}&query=Novosibirsk')
    dict_weather = json.loads(weather.text)
    temp, feel_temp = dict_weather['current']['temperature'], dict_weather['current']['feelslike']
    text = f'Погода в Новосибирске сейчас: {temp}. Ощущается как: {feel_temp}.'
    
    data = {'chat_id': chat_id, 'reply_to_message_id': message_id, 'text': text}
    requests.post(url, data=data)
    
@app.route('/')
def create_webhook():
    token = os.environ['TELEGRAM_TOKEN']
    method = 'setWebhook'
    web = 'https://flask-task-kambelloid.onrender.com/'
    data = {'url': web}
    return requests.get(f'https://api.telegram.org/bot{token}/{method}', data=data).content
    
@app.route('/', methods=['GET', 'POST'])
def receive_update():
    if request.method == 'POST':
        print(request.json)
        chat_id = request.json['message']['chat']['id']
        message_id = request.json['message']['message_id']
        send_message(chat_id, message_id)
    return {'ok': True}
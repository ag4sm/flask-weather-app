import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=77815caa8e7c8be3bf2e907b35a9817f'
    city = 'Atlanta'

    r = requests.get(url.format(city)).json()
    weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'feels like': r['main']['feels_like'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
        'humidity': r['main']['humidity'],
        'sunrise': r['sys']['sunrise'],
        'sunset': r['sys']['sunset']
    }
    print(weather)

    return render_template('weather.html')
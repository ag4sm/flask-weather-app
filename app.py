import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")

# Register database to app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/')
def index_get():
    cities = City.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=77815caa8e7c8be3bf2e907b35a9817f'

    weatherdata = []

    for city in cities:

        r = requests.get(url.format(city.name)).json()
        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'feels like': r['main']['feels_like'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'humidity': r['main']['humidity'],
            'sunrise': r['sys']['sunrise'],
            'sunset': r['sys']['sunset']
        }

        weatherdata.append(weather)

    return render_template('weather.html',weather=weatherdata)

@app.route('/', methods=['POST'])
def index_post():
    err_msg = ""
    new_city = request.form.get('city')

    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()
        
        if not existing_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()
        else:
            err_msg = "City already exists!"

    return redirect(url_for('index_get'))
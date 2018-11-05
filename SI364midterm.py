###############################
####### SETUP (OVERALL) #######
###############################
#matthew wolfgram - SI 364
#i referenced HW3, HW1, and Lectures 5-8

## Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError # **Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import secrets

## App setup code
app = Flask(__name__)
app.debug = True

## All app.config values
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string from si364'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/364midterm"
## Provided:
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

######################################
######## HELPER FXNS (If any) ########
######################################

def get_or_create_city(city, state, country): #latitude, longitude, country_id1, weather_time, humidity, icon_code, atm_pressure, temp_degc, temp_degf, wind_direct, wind_speed_ms, wind_speed_mph, country_id2, pollution_time, us_aqi, us_main, cn_aqi, cn_main): #make sure this function is only accepting city, state, country -- put this in the view fn before data collection?
    city = db.session.query(Location).filter_by(city = city).first()
    if city:
        return True
    if not city: #else?
        return False

##################
##### MODELS #####
##################

class AirVizWeatherData(db.Model):

    __tablename__ = "air visual weather data"
    id = db.Column(db.Integer, primary_key = True)
    country_id1 = db.Column(db.Integer , db.ForeignKey('location.id'))
    weather_time = db.Column(db.String(100))
    humidity = db.Column(db.Integer) #would it ever be a float??
    icon_code = db.Column(db.String(100))
    atm_pressure = db.Column(db.Integer)
    temp_degc = db.Column(db.Float)
    temp_degf = db.Column(db.Float) #this conversion is calculated upon data collection
    wind_direct = db.Column(db.Float)
    wind_speed_ms = db.Column(db.Float)
    wind_speed_mph = db.Column(db.Float)

    def __repr__(self): #this takes apart the object that is returned and formats it so it's legible
        return "location code: {} | timestamp: {} | temperature(deg.c): {} | temperature (deg.f): {} | humidity: {} | atmospheric pressure in hPa: {} | wind speed (mph): {} | ".format(self.country_id1, self.weather_time, self.temp_degc, self.temp_degf, self.humidity, self.atm_pressure, self.wind_speed_mph)

class AirVizPollutionData(db.Model):
    #add city id as foreign key? multiple one to many relationships -- city id and particulate classifiers
    __tablename__ = "air visual pollution data"
    id = db.Column(db.Integer, primary_key = True)
    country_id2 = db.Column(db.Integer , db.ForeignKey('location.id'))
    pollution_time = db.Column(db.String(100))
    us_aqi = db.Column(db.Integer)
    us_main = db.Column(db.String(100))
    cn_aqi = db.Column(db.Integer)
    cn_main = db.Column(db.String(100))

    def __repr__(self): #this takes apart the object that is returned and formats it so it's legible
        return "location code: {} | timestamp: {} | AQI from US: {} | main pollutant from US AQI: {} | AQI from CN: {} | main pollutant from CN AQI: {} | ".format(self.country_id2, self.pollution_time, self.us_aqi, self.us_main, self.cn_aqi, self.cn_main)

class Location(db.Model):

    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    linker1 = db.relationship('AirVizWeatherData', backref = 'Location')
    linker2 = db.relationship('AirVizPollutionData', backref = 'Location')

    def __repr__(self):
        return "{}, {} ({}) - location code: {}".format(self.city, self.state, self.country, self.id) #make this the first element of a tuple output?

###################
###### FORMS ######
###################

class CityForm(FlaskForm):
    city = StringField("enter a city somewhere in the US or China: ", validators = [Required(), Length(max = 280)])
    state = StringField("enter the state/province of your city: ", validators = [Required(), Length(max = 64)])
    country = StringField("enter the country your city is in (if it's in the united states, you must type 'USA' — if in China, just type 'China'): ", validators = [Required(), Length(max = 15)]) #link to list/page? of A3 codes??
    submit = SubmitField("submit")

    def validate_username(self, field):
        result = field.data
        split_display = result.split(' ')
        if "China" and "USA" not in split_display:
            raise ValidationError("your city must be in either the united states or china!")

    def validate_display_name(self, field):
        result = field.data
        split_display = result.split(' ')
        if len(split_display) > 7:
            raise ValidationError("display name can't exceed 7 words!")

#######################
###### VIEW FXNS ######
#######################

master_list = []
@app.route('/', methods = ['GET', 'POST'])
def index():
    form = CityForm(request.form)
    return render_template('index.html',form=form)

@app.route('/results', methods = ['GET', 'POST'])
def results():
    form = CityForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():

        try:
            city_test = form.city.data
            state_test = form.state.data
            country_test = form.country.data

            baseurl = "http://api.airvisual.com/v2/city?city={}&state={}&country={}&key={}".format(city_test, state_test, country_test, secrets.api_secret)

            response = requests.get(baseurl)
            data = json.loads(response.text)
            big_data = data['data']

            #individual elements from response

            city = big_data['city']         #city name
            state = big_data['state']       #state name
            country = big_data['country']   #country

            coor = big_data['location']['coordinates']
            lat = coor[0]   #latitude
            long = coor[1]  #longitude

            weather_ts = big_data['current']['weather']['ts']           #timestamp of weather data
            humidity = int(big_data['current']['weather']['hu'])        #humidity!
            icon_code = big_data['current']['weather']['ic']            #icon code for pic
            atm_pressure = int(big_data['current']['weather']['pr'])    #atm pressure in hPa
            temp_degc = int(big_data['current']['weather']['tp'])       #deg c temp
            temp_degf = ((temp_degc)*(9/5)) + 32                        #deg f temp
            wind_direct = int(big_data['current']['weather']['wd'])     #wind direction in deg
            wind_speed_ms = int(big_data['current']['weather']['ws'])   #wind speed (m/s)
            wind_speed_mph = (int(wind_speed_ms)*2.237)                 #wind speed (mph)

            pollution_ts = big_data['current']['pollution']['ts']       #timestamp of pollution data
            usaqi = int(big_data['current']['pollution']['aqius'])      #AQI val from EPA
            usmain = big_data['current']['pollution']['mainus']         #main pollutant -- see scale!
            cnaqi = int(big_data['current']['pollution']['aqicn'])      #AQI val from China's MEP standard
            cnmain = big_data['current']['pollution']['maincn']         #main pollutant from MEP metric


            if get_or_create_city(city, state, country) == True:
                #pass
                flash("!!!! this city already exists! enter another one! ")
                return redirect(url_for('index'))

            if get_or_create_city(city, state, country) == False:

                city = Location(city = city, state = state, country = country, latitude = lat, longitude = long) #wait is there fkey
                db.session.add(city)
                db.session.commit()

                weather = AirVizWeatherData(country_id1 = city.id, weather_time = weather_ts, humidity = humidity, icon_code = icon_code, atm_pressure = atm_pressure, temp_degc = temp_degc, temp_degf = temp_degf, wind_direct = wind_direct, wind_speed_ms = wind_speed_ms, wind_speed_mph = wind_speed_mph)
                db.session.add(weather)
                db.session.commit()

                pollution = AirVizPollutionData(country_id2 = city.id, pollution_time = pollution_ts, us_aqi = usaqi, us_main = usmain, cn_aqi = cnaqi, cn_main = cnmain)
                db.session.add(pollution)
                db.session.commit() #only one commit?

            master_list.append((city, state, country, lat, long, weather_ts, humidity, icon_code, atm_pressure, temp_degc, temp_degf, wind_direct, wind_speed_ms, wind_speed_mph, pollution_ts, usaqi, usmain, cnaqi, cnmain))
            mlist1 = master_list[0:5]
            return(redirect(url_for('index')))

        except:
            flash("!!!! ERRORS IN FORM SUBMISSION! try again! ")
            return redirect(url_for('index'))

    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
        return redirect(url_for('index'))

@app.route('/allPollution')
def all_pollution():
    pollute = AirVizPollutionData.query.all()
    city = Location.query.all()
    return render_template('pollution.html', city = city, pollute = pollute)

@app.route('/allWeather')
def all_weather():
    weather = AirVizWeatherData.query.all()
    city = Location.query.all()
    return render_template('weather.html', city = city, weather = weather) 

#error handling -- taken from HW3
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)

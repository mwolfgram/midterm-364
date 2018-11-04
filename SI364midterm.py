###############################
####### SETUP (OVERALL) #######
###############################
#add name, code you referenced

## Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError # **Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required # Here, too
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
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/364midterm" #make a database name and then get the url, formatted as above
## Provided:
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################

#do this after models — your route will likely need a helper function



##################
##### MODELS #####
##################

class Location(db.Model):

    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    linker1 = db.Relationship('AirVizWeatherData', backref = 'Location')
    linker2 = db.Relationship('AirVizPollutionData', backref = 'Location')

    def __repr__(self):
        return "{}, {} ({})".format(self.city, self.state, self.country) #make this the first element of a tuple output?

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

#redo the whole "location code" thing so an actual country name is displayed
#^ or maybe just format the country name into the html?? who know, it shouldn't be an awful fix either way

###################
###### FORMS ######
###################

class CityForm(FlaskForm):
    city = StringField("enter a city somewhere in the world: ", validators = [Required(), Length(max = 280)])   ## -- text: tweet text (Required, should not be more than 280 characters)
    state = StringField("enter the state/province of your city: ", validators = [Required(), Length(max = 64)])               ## -- username: the twitter username who should post it (Required, should not be more than 64 characters)
    country = StringField("enter the country your city is in: ", validators = [Required()])                                             ## -- display_name: the display name of the twitter user with that username (Required, + set up custom validation for this -- see below)
    submit = SubmitField('remember: capitalism is the biggest reason for air pollution')

    def validate_username(self, field): #making sure no idiot says africa is a country
        result = field.data
        split_display = result.split(' ')
        if "Africa" in split_display: #***how to isolate the country for this validator?
            if "South Africa" or "Central African Republic" in split_display: #how does this split end up working?
                pass
            else:
                raise ValidationError("Africa is not a country >:(")

    def validate_display_name(self, field): #custom validation - the output can't be more than 7 words
        result = field.data
        split_display = result.split(' ')
        if len(split_display) > 7:
            raise ValidationError("display name can't exceed 7 words!")

#######################
###### VIEW FXNS ######
#######################

@app.route('/')
def home():
    form = CityForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if form.validate_on_submit():
        name = form.name.data
        newname = Name(name)
        db.session.add(newname)
        db.session.commit()
        return redirect(url_for('all_names'))
    return render_template('base.html',form=form)
    #***redirect(url_for('index'))

@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('name_example.html',names=names)




#error handling -- taken from HW3 -- put these above? does it matter?

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)

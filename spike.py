#spike.py

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import secrets

#what data can be accessed with a community key?
#say what api is used in the readme!
#index data points, figure out how to table them / what will be one-to-many
#which functinos fo what, how will they interact?
#templates! make sure there are loops and whatever else

# units : { //object containing units information
#       "p2": "ugm3", //pm2.5
#       "p1": "ugm3", //pm10
#       "o3": "ppb", //Ozone O3
#       "n2": "ppb", //Nitrogen dioxide NO2
#       "s2": "ppb", //Sulfur dioxide SO2
#       "co": "ppm" //Carbon monoxide CO }

def prelim():
    baseurl = "http://api.airvisual.com/v2/city?city=Los Angeles&state=California&country=USA&key={}".format(secrets.api_secret)
    #print(baseurl)
    #try formatting for every part of the url
    #

    #querystring = {"city":"Beijing","state":"Beijing","country":"China","key": "ih759G8bZXogKrbAA"}

    response = requests.get(baseurl) #, params=querystring)
    data = json.loads(response.text)
    big_data = data['data']

    ### individual elements

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


    print(data['data'])
    print('------------------------')
    print((city, state, country, coor, lat, long, weather_ts, humidity, icon_code, atm_pressure, temp_degc, temp_degf, wind_direct, wind_speed_ms, wind_speed_mph, pollution_ts, usaqi, usmain, cnaqi, cnmain))
    return(data['data'])

prelim()

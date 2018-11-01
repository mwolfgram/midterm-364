#spike.py

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import secrets

def prelim():
    baseurl = "http://api.airvisual.com/v2/city?city=Los Angeles&state=California&country=USA&key={}".format(secrets.api_secret)
    #print(baseurl)

    #querystring = {"city":"Beijing","state":"Beijing","country":"China","key": "ih759G8bZXogKrbAA"}

    response = requests.get(baseurl) #, params=querystring)
    data = json.loads(response.text)

    print(data)
    return(data)

prelim()

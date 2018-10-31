import os
from flask import Flask, render_template, session, redirect, url_for, request
from flask_script import Shell, Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell


# Configure base directory of app
basedir = os.path.abspath(os.path.dirname(__file__))

# Application configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364thisisnotsupersecurebutitsok'

# Update the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
db = SQLAlchemy(app) # For database use

#########
######### Everything above this line is important setup, not problem-solving.
#########

##### Set up Forms #####
class MovieDirectorForm(FlaskForm):
    movie_name = StringField('Enter movie name:', validators=[Required()])
    director_name = StringField('Enter director name:', validators=[Required()])
    submit = SubmitField('Submit')

##### Set up Models #####

class Movie(db.Model):
    __tablename__ = 'movies'
    movieId = db.Column(db.Integer, primary_key=True)
    movieTitle = db.Column(db.String(64))
    directorId = db.Column(db.Integer, db.ForeignKey('directors.directorId'))


class Director(db.Model):
    __tablename__ = 'directors'
    directorId = db.Column(db.Integer, primary_key=True)
    directorName = db.Column(db.String(128))


##### Set up Models #####
@app.route("/")
def index():
    form = MovieDirectorForm()
    return render_template("index.html", form = form)

#Add code to this function
@app.route("/addMovie")
def result():
    form = MovieDirectorForm(request.form)
    if form.validate_on_submit():
        movie_name = form.movie_name.data
        director_name = form.director_name.data
        d = Director.query.filter_by(directorName=director_name).first()
        if d:
            print("Director exists", d.directorId)
        else:
            d = Director(directorName = director_name)
            db.session.add(d)
            db.session.commit()

        m = Movie(movieTitle = movie_name, directorId = ddirectorId)
        db.session.add(m)
        db.session.commit()

        return render_template('movies.html')


#Add code to this function
@app.route("/viewMovies")
    moveis = Movie.query.all()


if __name__=='__main__':
    db.create_all()
    manager.run()
    app.run(debug = True)

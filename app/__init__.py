from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '83jhr.s/s83ebs.z.][#3ie-3=//d~'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///application.sqlite'
app.config['PERPAGE_MIN_LIMIT'] = 20
app.config['PERPAGE_MAX_LIMIT'] = 100
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

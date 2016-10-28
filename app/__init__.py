from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_settings

app = Flask(__name__)
app.config.from_object(config_settings['development'])
db = SQLAlchemy(app)

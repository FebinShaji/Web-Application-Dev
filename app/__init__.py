from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import logging

logging.basicConfig(filename='StudentReads.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)
app.config.from_object('config')

csrf = CSRFProtect(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import views, models

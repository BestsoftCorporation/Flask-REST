# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:marko@localhost/data_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db=SQLAlchemy(app)

db.create_all()

migrate = Migrate(app, db)
from app import routes, models


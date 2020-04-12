from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_uri = 'postgresql://romain@localhost:5432/gym'

app = Flask(import_name='Hello world')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app=app)

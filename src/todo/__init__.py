from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db_uri = 'postgresql://romain@localhost:5432/todo'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

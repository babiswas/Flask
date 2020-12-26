from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SECRET_KEY']='I am Bapan'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:36network@localhost/grocery'
db=SQLAlchemy(app)
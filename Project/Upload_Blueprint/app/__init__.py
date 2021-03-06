from flask import Flask
from app import home_route
from . import blueprintutil
from config import Config

def create_app():
   app=Flask(__name__)
   app.register_blueprint(blueprintutil.app1)
   app.config.from_object(Config)
   return app

   
   
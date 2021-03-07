from flask import Flask
from config import Config
from . import blueprintutil
from app import task_route
from .import taskapp






def create_app():
   app=Flask(__name__)
   app.config.from_object(Config)
   app.register_blueprint(blueprintutil.taskgenerator)
   return app

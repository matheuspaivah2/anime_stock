from flask import Flask
from environs import Env
from app.services import check_if_exists_and_create_table_animes
from app import views

env = Env()
env.read_env()
check_if_exists_and_create_table_animes()

def create_app():
    app = Flask(__name__)

    views.init_app(app)

    return app
from flask import Flask
from dotenv import load_dotenv

from config import Config
from .db import close_db
from .routes import bp


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    app.register_blueprint(bp)
    app.teardown_appcontext(close_db)
    return app

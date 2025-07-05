from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from .database import db
from .routes import api
from .models import Job  # Required

migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app)
    app.register_blueprint(api)

    return app

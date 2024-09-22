from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes_main import main
    from app.routes_form import form
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(form)
    app.register_blueprint(auth)

    return app
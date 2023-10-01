import os
from flask import Flask
from . import db
from . import mail

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DATABASE_HOST=os.environ.get("FLASK_DATABASE_HOST"),
        DATABASE_PASSWORD=os.environ.get("FLASK_DATABASE_PASSWORD"),
        DATABASE_USER=os.environ.get("FLASK_DATABASE_USER"),
        DATABASE=os.environ.get("FLASK_DATABASE"),
        MY_ADDRESS = os.environ.get("MY_ADDRESS"),
        PASSWORD=os.environ.get("PASSWORD")
    )

    db.init_app(app)
    app.register_blueprint(mail.bp)

    return app
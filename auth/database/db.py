from circuitbreaker import circuit
from core.config import TestSettings
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
settings = TestSettings()


jwt = JWTManager()

db = SQLAlchemy()


@circuit
def init_db(app: Flask):
    with app.app_context():
        db.create_all()
    db.init_app(app)

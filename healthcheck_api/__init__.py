import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    @app.route("/")
    @app.route("/healthcheck")
    def healthcheck():
        try:
            db.session.query(text('1')).from_statement(text('SELECT 1')).all()
            return { "success": True }
        except Exception as e:
            return { "error": str(e) }, 500

    return app

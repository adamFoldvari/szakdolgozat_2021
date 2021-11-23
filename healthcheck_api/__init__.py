import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    from healthcheck_api.entries import EntryModel

    @app.route("/")
    @app.route("/healthcheck")
    def healthcheck():
        try:
            db.session.query(text('1')).from_statement(text('SELECT 1')).all()
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/entries', methods=['GET'])
    def handle_entries():
        if request.method == 'GET':
            entries = EntryModel.query.all()
            return jsonify(entries), 200

    return app

# app.py — Application factory with SQLAlchemy and Flask-Migrate wired in.

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialise extensions outside create_app so models can import 'db'
# without triggering a circular import
db      = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from courses.routes import courses_bp
    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'status': 'error', 'message': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'status': 'error', 'message': 'Server error'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

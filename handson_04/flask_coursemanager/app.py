from flask import Flask, jsonify
from config import AppConfig
from courses.routes import courses_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def not_found(err):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def server_error(err):
        return jsonify({'error': 'Internal server error'}), 500

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(debug=True)

# app.py — Application factory entry point.
# The factory pattern (create_app function) is Flask best practice:
# it avoids circular imports and makes the app easy to test by letting
# you create multiple instances with different configs.

from flask import Flask, jsonify
from config import Config
from courses.routes import courses_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register the courses blueprint — all /api/courses/* routes come from here
    app.register_blueprint(courses_bp)

    # JSON error handlers — APIs should never return HTML error pages.
    # Flask's default errors are HTML, so we override them explicitly.
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

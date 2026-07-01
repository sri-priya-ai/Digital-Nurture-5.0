from flask import Flask, jsonify
from config import AppConfig
from extensions import db, migrate_ext
from courses.routes import courses_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    db.init_app(app)
    migrate_ext.init_app(app, db)

    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def handle_500(err):
        return jsonify({'error': 'Server error'}), 500

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(debug=True)

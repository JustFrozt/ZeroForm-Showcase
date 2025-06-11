# __init__.py

from flask import Flask, jsonify
from .extensions import db, ma, jwt, bcrypt, flasgger, migrate, limiter
from .config import Config


def create_app(config_class=Config):
    """
    Application factory function.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- Initialize Extensions ---
    # Each extension is initialized with the Flask app instance.

    db.init_app(app)
    # Link the migration engine to the app and the database
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    # Initialize the rate limiter
    limiter.init_app(app)

    # --- Swagger/Flasgger API Documentation Configuration ---
    app.config["SWAGGER"] = {
        "title": "Flask Notes API",
        "uiversion": 3,
        "specs_route": "/apidocs/",
        "definitions": {
            "Note": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "The note ID."},
                    "title": {"type": "string", "description": "The title of the note."},
                    "content": {"type": "string", "description": "The content of the note."},
                    "date_posted": {"type": "string", "format": "date-time", "description": "The timestamp of when the note was created."},
                    "user_id": {"type": "integer", "description": "The ID of the user who owns the note."}
                }
            }
        },
        "securityDefinitions": {"Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}}
    }
    flasgger.init_app(app)


    # --- Register Blueprints ---

    from .routes.auth import auth_bp
    from .routes.notes import notes_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(notes_bp, url_prefix="/api")


    # --- Register Error Handlers ---
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"message": "The requested resource was not found."}), 404

    @app.errorhandler(500)
    def internal_error(error):

        return jsonify({"message": "An unexpected internal server error occurred."}), 500

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return jsonify({"message": "The method is not allowed for the requested URL."}), 405


    return app
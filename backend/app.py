from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # CORS configuration to allow requests from the frontend
    CORS(
        app,
        resources={r"/*": {"origins": "http://localhost:3000"}},
        supports_credentials=True,
    )

    # Import models here to ensure they are registered before creating tables
    with app.app_context():
        # Import models
        from models import User, List, Item

        # Create database tables
        db.create_all()

        # Register blueprints
        from routes.auth_routes import auth_bp
        from routes.list_routes import list_bp
        from routes.item_routes import item_bp

        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(list_bp, url_prefix="/lists")
        app.register_blueprint(item_bp, url_prefix="/items")

        # Root route
        @app.route("/")
        def home():
            return {"message": "Welcome to the Hierarchical Todo List API!"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
# Compare this snippet from backend/routes/item_routes.py:

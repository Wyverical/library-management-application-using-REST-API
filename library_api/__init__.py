# library_api/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from . import models  # Ensure models are imported so that tables can be created
        db.create_all()

    # Register blueprints for modular routes
    from .routes.auth import auth_bp
    from .routes.users import users_bp
    from .routes.books import books_bp
    from .routes.transactions import transactions_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')

    @app.route('/')
    def index():
        return "Library Management System API is running", 200

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.api.users import users_bp
    from app.api.tasks import tasks_bp

    app.register_blueprint(users_bp, url_prefix="/api/v1/users")
    app.register_blueprint(tasks_bp, url_prefix="/api/v1/tasks")

    return app
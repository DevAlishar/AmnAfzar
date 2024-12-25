from flask import Flask, jsonify
from flasgger import Swagger
from flask_migrate import Migrate
from app.models.models import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    swagger = Swagger(app, template={
        "info": {
            "title": "To Do List API",
            "version": "1.0.0",
        },
    })

    # Register blueprints
    from app.api.users import users_bp
    from app.api.tasks import tasks_bp

    app.register_blueprint(users_bp, url_prefix="/api/v1/users")
    app.register_blueprint(tasks_bp, url_prefix="/api/v1/tasks")

    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(swagger(app))

    return app
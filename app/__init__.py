from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    
    # Register blueprints
    from app.routes.tickets import tickets_bp
    from app.routes.linkedin import linkedin_bp
    from app.routes import home_bp
    app.register_blueprint(tickets_bp)
    app.register_blueprint(linkedin_bp)
    app.register_blueprint(home_bp)

    return app

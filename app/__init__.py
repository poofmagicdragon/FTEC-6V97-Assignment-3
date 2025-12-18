from flask import Flask
#from .routes.portfolio import portfolio_bp
#from app.service.database import db
#from app.config import DevelopmentConfig
from app.db import db
from app.routes.portfolio_bp import portfolio_bp
from app.routes.security_bp import security_bp
from app.routes.user_bp import user_bp

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    #Register blueprints
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(user_bp)

    return app


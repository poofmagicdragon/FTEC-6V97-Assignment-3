from flask import Blueprint
#from app.extensions import db
from app.domain import User

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return{"message": "Hello from Flask + SQLAlchemy"}

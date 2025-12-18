from flask import Blueprint, request
#from app.service.user_service import 
from app.db import db
from app.service.user_service import get_all_users, get_user_by_username, create_user, delete_user

user_bp = Blueprint('user', __name__, url_prefix='/user') 

# 1.
@user_bp.route('/get_all_users', methods = ['GET'])
def get_all_users_route():
    try:
        users = get_all_users(db.session)

        output = [{
            "username": u.username,
            "firstname": u.firstname,
            "lastname": u.lastname,
            "password": u.password,
            "balance": u.balance
        } for u in users]

        return {"users": output}, 201
    except Exception as e:
        return {"error": e}, 400

# 2.
@user_bp.route('/get_user_by_id/<username>', methods = ['GET'])
def get_user_by_id_route(username):
    try:
        user = get_user_by_username(username, db.session)

        output = [{
            "username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "password": user.password,
            "balance": user.balance
        }]
        return {"user": output}, 201
    except Exception as e:
        return {"error": e}, 400
    
# 3.
@user_bp.route('/create_user', methods = ['POST'])
def create_user_route():
    data = request.get_json()
    try:
        user_dict = {
        "username": data.get("username"),
        "firstname": data.get("firstname"),
        "lastname": data.get("lastname"),
        "password": data.get("password"),
        "balance": data.get("balance")
        }

        message = create_user(db.session, user_dict)
        return {"message": message}, 201
    except Exception as e:
        return {"error": e}, 400

# 4.
@user_bp.route('/delete_user/<username>', methods = ['DELETE'])
def delete_user_route(username):
    try:
        message = delete_user(db.session, username)
        return {"message": message}, 201
    except Exception as e:
        return {"error": e}, 400


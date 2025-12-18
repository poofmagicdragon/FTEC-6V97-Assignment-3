from flask import Blueprint, request
from app.service.security_service import get_all_securities
from app.db import db

security_bp = Blueprint('security', __name__, url_prefix = '/security')

# 1.
@security_bp.route('/get_all_securities', methods = ['GET'])
def get_all_securities_route():
    try:
        securities = get_all_securities(db.session)
        output = [{
            "ticker": s.ticker,
            "issuer": s.issuer,
            "price": s.price
        } for s in securities]

        return {"securities": output}, 201
    except Exception as e:
        return {"error": str(e)}, 400

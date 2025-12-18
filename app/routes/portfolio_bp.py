from flask import Blueprint, request
from app.service.portfolio_service import create_portfolio, get_all_portfolios, get_portfolio_by_id, delete_portfolio
from app.service.investment_service import create_purchase_order, harvest_investment
from app.db import db
from app.domain.User import User


portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio') 

# 1.
@portfolio_bp.route('/create', methods=['POST'])
def create_portfolio_route():
    data = request.get_json()
    try:
        name = data.get('name')
        description = data.get('description')
        owner = data.get('owner')
        investment_strategy = data.get('investment_strategy')

        message = create_portfolio(owner, name, description, investment_strategy)
        return {"message": message}, 201
    except Exception as e:
        return {"error": str(e)}, 400

# 2.     
@portfolio_bp.route('/get_all_portfolios', methods = ['GET'])
def get_all_portfolios_route():
    try:
        portfolios = get_all_portfolios(db.session)

        output = [{
            "id":p.id,
            "owner":p.owner,
            "name":p.name,
            "description":p.description,
            "investment":p.investment_strategy
        } for p in portfolios]

        return {"portfolios": output}, 201
    except Exception as e:
        return {"error": str(e)}, 400

# 3. 
@portfolio_bp.route('/get_portfolio_by_id/<int:portfolio_id>', methods = ['GET'])
def get_portfolio_by_id_route(portfolio_id):    
    try:
        portfolio = get_portfolio_by_id(db.session, portfolio_id)
        output = {            
            "id":portfolio.id,
            "owner":portfolio.owner,
            "name":portfolio.name,
            "description":portfolio.description,
            "investment":portfolio.investment_strategy}
        return {"portfolio": output}, 201
    except Exception as e:
        return {"error": str(e)}, 400

# 4.
@portfolio_bp.route('/delete_portfolio/<portfolio_name>/<user_name>', methods = ['DELETE'])
def delete_portfolio_route(portfolio_name, user_name):
    try:
        message = delete_portfolio(db.session, portfolio_name, user_name)
        return {"message": message}, 201
    except Exception as e:
        return {"error": str(e)}, 400

# 5.
@portfolio_bp.route('/add_security_to_portfolio/<int:portfolio_id>', methods=['POST'])
def add_security_to_portfolio_route(portfolio_id):
    data = request.get_json()
    try:
        ticker = data.get("ticker")
        quantity_to_buy = int(data.get("quantity"))
        username = data.get("user")

        user = db.session.query(User).filter_by(username=username).one_or_none()
        if user is None:
            return {"error": f"User '{username}' not found"}, 404

        message = create_purchase_order(db.session, user.username, portfolio_id, ticker.upper(), quantity_to_buy, user.balance)
        return {"message": message}, 201

    except Exception as e:
        return {"error": str(e)}, 400

# 6.
@portfolio_bp.route('/harvest_investment/<int:portfolio_id>', methods = ['POST'])
def harvest_investment_route(portfolio_id):
    data = request.get_json()
    try:
        ticker = data.get("ticker")
        quantity_to_sell = data.get("quantity_to_sell")
        sell_price = data.get("sell_price")
        username = data.get("user")

        user = db.session.query(User).filter_by(username=username).one_or_none()
        if user is None:
            return {"error": f"User '{username}' not found"}, 404
        
        message = harvest_investment(db.session, user.username, portfolio_id, ticker, quantity_to_sell, sell_price, user.balance)
        return{"message": message}, 201
    except Exception as e:
        return {"error": str(e)}, 400        


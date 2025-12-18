from pytest import Session
from rich.console import Console
from app.domain import Investment, User, Transaction
from app.domain.Portfolio import Portfolio
from rich.table import Table
from typing import List
from sqlalchemy.exc import IntegrityError
from app.domain.security import Security 
from app.service.user_service import get_logged_in_user, update_user_balance
from app.database import get_session
from app.db import db
from sqlalchemy import func


_console = Console()

class UnsupportedUserOperationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)



# def create_portfolio(session: Session, user: User) -> str:
#     try:
#         name = _console.input("Portfolio name: ")
#         description = _console.input("Portfolio description: ")
#         investment_strategy = _console.input("Investment Strategy: ")
#         session.add(Portfolio(owner = user.username, name = name, description = description, investment_strategy = investment_strategy))
#         session.commit()
#         return f"Portfolio {name} created successfully"
#     finally:
#         session.close()

def create_portfolio(owner: str, session: Session,name: str, description: str, investment_strategy: str) -> str:
    portfolio = Portfolio(owner = owner, name = name, description = description, investment_strategy = investment_strategy)
    try:
        session.add(portfolio)
        session.commit()
        return f"Portfolio {name} created successfully"
    finally:
        session.close()
    
def get_portfolio_by_name(name: str, session: Session, owner: str) -> Portfolio |None:
    portfolio = session.query(Portfolio).filter_by(name=name, owner = owner).one_or_none()
    return portfolio

def get_portfolio_by_id(session: Session, id: int) -> Portfolio |None:
    portfolio = session.query(Portfolio).filter_by(id = id).one_or_none()
    return portfolio


def get_all_portfolios(session: Session) -> List[Portfolio]:
    try:
        portfolios = session.query(Portfolio).all()
        return portfolios
    finally:
        session.close()


# def get_holdings_value(portfolio: Portfolio) -> float:
#     value = 0.0
#     for ticker, quantity in portfolio.holdings.items():
#         security = db.get_security_by_ticker(ticker)
#         if security:
#             value += security.price * quantity
#     return value

def print_all_portfolios(session: Session) -> None:    
    try:
        portfolios = session.query(Portfolio).filter_by(owner = get_logged_in_user().username).all()
        if len(portfolios) == 0:
            return _console.print("No portfolios exist. Add new portfolios", style = "red")    
        
        table = Table(title = "Portfolios")
        table.add_column("Portfolio ID", style = "orange3")
        table.add_column("Owner", style = "bold cyan")
        table.add_column("Name", style = "bold cyan")
        table.add_column("Description", style = "orchid")
        table.add_column("Investment strategy", style = "orchid")
        #table.add_column("Holdings value", style = "green")
        table.add_column("Investments", style = "green")


        for portfolio in portfolios:
            investments = session.query(Investment).filter_by(portfolio_id=portfolio.id).all()
            investment_dicts = [{"ticker": inv.ticker, "quantity": inv.quantity,} for inv in investments]
            investments_str = ", ".join(f"{inv['ticker']} ({inv['quantity']})" for inv in investment_dicts)
            
            table.add_row(str(portfolio.id), portfolio.owner, portfolio.name, portfolio.description, portfolio.investment_strategy, investments_str)
        _console.print(table)
    finally:
        session.close()

def get_portfolio_name_for_deletion() -> str:
    return input("Enter the portfolio name to delete: ").strip()
    

def delete_portfolio(session: Session, portfolio_name: str, username: str) -> str:
    # Temporarily commented out for Assignment 3
    #user = get_logged_in_user()
    portfolio = get_portfolio_by_name(portfolio_name, session, username)

    if portfolio is None:
        raise UnsupportedUserOperationError(f"Portfolio '{portfolio_name}' does not exist")

    investments = session.query(Investment).filter_by(portfolio_id=portfolio.id).all()

    if any(inv.quantity > 0 for inv in investments):
        raise UnsupportedUserOperationError(
            f"Portfolio '{portfolio_name}' still has active investments and cannot be deleted"
        )

    session.delete(portfolio)
    session.commit()
    return f"Portfolio '{portfolio_name}' deleted successfully"   

def get_all_portfolio_logged_in_user(session: Session, username: str) -> List[Portfolio]:
    user = db.session.query(User).filter_by(username=username).one_or_none()
    portfolios = session.query(Portfolio).filter_by(owner = user.username).all()
    return portfolios

# # This was for assignment three.  The other function is in the investment_service module
# def add_security_to_portfolio(session: Session, portfolio_id: int, ticker: str, quantity: int) -> str:
#     portfolio = session.query(Portfolio).filter_by(id=portfolio_id).first()
#     if portfolio is None:
#         raise UnsupportedUserOperationError(f"Portfolio with id {portfolio_id} does not exist")

#     new_investment = Investment(
#         portfolio_id=portfolio.id,
#         ticker=ticker,
#         quantity=quantity,
#     )

#     session.add(new_investment)
#     session.commit()

#     return f"Added {quantity} of {ticker} to portfolio '{portfolio.name}'"

# # for Assignment 3 usage
# def harvest_investment(session: Session, portfolio_id: str, ticker: str, quantity_to_sell: int, sell_price: int) -> str:

#      # Step 1: Find the portfolio
#     portfolio = session.query(Portfolio).filter_by(id=portfolio_id).one_or_none()
#     if portfolio is None:
#         raise UnsupportedUserOperationError(f"Portfolio with id {portfolio_id} does not exist")

#     # Step 2: Get the owner (User object via relationship)
#     user = portfolio.user
#     if user is None:
#         raise UnsupportedUserOperationError(f"Portfolio {portfolio_id} has no valid owner")



#     try:
#         portfolio_id = int(portfolio_id)
#     except ValueError:
#         _console.print(f"Invalid input: '{portfolio_id}' is not a number")
#         return f"Invalid input: '{portfolio_id}' is not a number"
    
#     if portfolio_id not in [p.id for p in get_all_portfolio_logged_in_user(session)]:
#         _console.print(f"Portfolio ID {portfolio_id} does not exist.  Please enter a valid portfolio ID", style="red")
#         return f"Portfolio ID {portfolio_id} does not exist.  Please enter a valid portfolio ID"


#     number_of_shares = session.query(func.sum(Investment.quantity)).filter_by(portfolio_id = portfolio_id, ticker = ticker).scalar()
#     number_of_shares = number_of_shares or 0

#     if number_of_shares == 0:
#         _console.print(f"Portfolio {portfolio_id} does not have any shares of {ticker}")
#         return f"Portfolio {portfolio_id} does not have any shares of {ticker}"

 

#     if number_of_shares < quantity_to_sell:
#         _console.print("Insufficient quantity to make sale", style="bold red")
#         return "Insufficient quantity to make sale"

#     sell_price = float(sell_price)

#     number_of_shares -= quantity_to_sell
#     investment = session.query(Investment).filter_by(portfolio_id = portfolio_id, ticker = ticker).first()
#     investment.quantity = number_of_shares

#     transaction = Transaction(user_id = user.username, portfolio_id = portfolio_id, security_id = ticker, trans_type = "SELL", quantity = quantity_to_sell, price = sell_price)
#     session.add(transaction)

#     new_balance = user.balance + (sell_price * quantity_to_sell)
#     update_user_balance(session, user.username, new_balance)
#     return f"Created and executed new sell order for {quantity_to_sell} shares of {ticker} in portfolio {portfolio_id} for ${sell_price}"






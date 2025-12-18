from app.domain import Transaction
from rich.console import Console
from sqlalchemy.orm import Session
from rich.table import Table
from app.service.user_service import get_logged_in_user
from typing import List

_console = Console()

def get_all_transactions(session: Session) -> List[Transaction]:
    try:
        transactions = session.query(Transaction).all()
        return transactions
    finally:
        session.close()

def print_all_transactions(session: Session) -> None:    
    try:
        transactions = session.query(Transaction).filter_by(user_id = get_logged_in_user().username).all()
        if len(transactions) == 0:
            return _console.print("No transactions exist. Make a transaction", style = "red")    
        table = Table(title = "Transactions")        
        table.add_column("ID")
        table.add_column("User ID")
        table.add_column("Portfolio ID")
        table.add_column("security ID")
        table.add_column("Transaction Type")    
        table.add_column("Quantity")
        table.add_column("Price")
        table.add_column("Time Stamp")
        for transaction in transactions: 
            table.add_row(str(transaction.id), str(transaction.user_id), str(transaction.portfolio_id), str(transaction.security_id), str(transaction.trans_type), str(transaction.quantity), str(transaction.price), str(transaction.timestamp))
        _console.print(table)
    finally:
        session.close()
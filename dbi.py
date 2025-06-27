"""
database interactions
"""

from sqlalchemy.orm import Session
from schemas import SQLATransaction, Transaction


class DBI:
    """
    Class to handle database interactions.
    """

    def __init__(self, db: Session):
        self.db = db

    def add_transaction(self, transaction: Transaction) -> SQLATransaction:
        """
        Add a new transaction to the database.
        """
        db_transaction = SQLATransaction(**transaction.model_dump())
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction
    
    def update_transaction(self, transaction: Transaction) -> SQLATransaction:
        """
        Update an existing transaction in the database.
        """
        db_transaction = self.db.query(SQLATransaction).filter(
            SQLATransaction.id == transaction.id
        ).first()
        
        if not db_transaction:
            raise ValueError("Transaction not found")
        
        for key, value in transaction.model_dump().items():
            setattr(db_transaction, key, value)
        
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

    def get_transaction(self, transaction_id: int) -> SQLATransaction:
        """
        Retrieve a transaction by its ID.
        """
        db_transaction = self.db.query(SQLATransaction).filter(
            SQLATransaction.id == transaction_id
        ).first()
        
        if not db_transaction:
            raise ValueError("Transaction not found")
        
        return db_transaction
    
    def delete_transaction(self, transaction_id: int) -> None:
        """
        Delete a transaction by its ID.
        """
        db_transaction = self.db.query(SQLATransaction).filter(
            SQLATransaction.id == transaction_id
        ).first()
        
        if not db_transaction:
            raise ValueError("Transaction not found")
        
        self.db.delete(db_transaction)
        self.db.commit()

    def get_all_transactions(self) -> list[SQLATransaction]:
        """
        Retrieve all transactions from the database.
        """
        return self.db.query(SQLATransaction).all()

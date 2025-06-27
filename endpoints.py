"""
module to configure endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dbi import DBI
from schemas import Transaction, SQLATransaction
from database import SessionLocal, engine, Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    """create new session on request and closes on completion"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def root():
    """Root endpoint"""
    logging.info("Root endpoint accessed")
    return {"message": "Welcome to the Budget API!"}

@router.post("/transactions/", response_model=Transaction)
async def create_transaction(
    transaction: Transaction, db: Session = Depends(get_db)
):
    """
    Create a new transaction.
    """
    logging.info(f"Creating transaction: {transaction}")
    try:
        return DBI(db).add_transaction(transaction)
    except Exception as e:
        logging.error(f"Error creating transaction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.put("/transactions/{transaction_id}", response_model=Transaction)
async def update_transaction(
    transaction_id: int, transaction: Transaction, db: Session = Depends(get_db)
):
    """
    Update an existing transaction.
    """
    logging.info(f"Updating transaction ID {transaction_id}: {transaction}")
    try:
        transaction.id = transaction_id  # Ensure the ID is set for the update
        return DBI(db).update_transaction(transaction)
    except ValueError as e:
        logging.error(f"Transaction not found: {e}")
        raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        logging.error(f"Error updating transaction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(
    transaction_id: int, db: Session = Depends(get_db)
):
    """
    Retrieve a transaction by its ID.
    """
    logging.info(f"Retrieving transaction ID {transaction_id}")
    try:
        return DBI(db).get_transaction(transaction_id)
    except ValueError as e:
        logging.error(f"Transaction not found: {e}")
        raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        logging.error(f"Error retrieving transaction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.delete("/transactions/{transaction_id}")
async def delete_transaction(
    transaction_id: int, db: Session = Depends(get_db)
):
    """
    Delete a transaction by its ID.
    """
    logging.info(f"Deleting transaction ID {transaction_id}")
    try:
        DBI(db).delete_transaction(transaction_id)
        return {"message": "Transaction deleted successfully"}
    except ValueError as e:
        logging.error(f"Transaction not found: {e}")
        raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        logging.error(f"Error deleting transaction: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/transactions/", response_model=list[Transaction])
async def get_all_transactions(db: Session = Depends(get_db)
):
    """
    Retrieve all transactions.
    """
    logging.info("Retrieving all transactions")
    try:
        return DBI(db).get_all_transactions()
    except Exception as e:
        logging.error(f"Error retrieving transactions: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
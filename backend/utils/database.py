# util/database.py
from contextlib import contextmanager
from app.extensions import db

@contextmanager
def safe_transaction():
    """Handle database transactions with automatic commit on completion & rollback on error"""
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise  
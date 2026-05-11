# util/database.py
from contextlib import contextmanager
from backend.app.extensions import db

@contextmanager
def safe_transaction():
    """Handle database transactions with automatic rollback on error"""
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise  
from functools import wraps
from flask import jsonify
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, SQLAlchemyError
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden
import traceback
import logging
from exstensions import db

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        # User-facing errors (safe to show)
        except (BadRequest, ValueError, TypeError):
            return jsonify({'error': 'Invalid request'}), 400
        except Unauthorized:
            return jsonify({'error': 'Unathorized. Access Denied'}), 401
        except Forbidden:
            return jsonify({'error': 'You are not allowed to do that.'}), 403

        # Database errors (log only, hide message)
        except (IntegrityError, DataError, OperationalError, SQLAlchemyError) as e:
            db.session.rollback()
            logging.error(f"Database Error: {e}\n{traceback.format_exc()}")
            return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

        # Catch-all for anything else
        except Exception as e:
            db.session.rollback()
            logging.error(f"Unhandled Error: {e}\n{traceback.format_exc()}")
            return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500
    return wrapper
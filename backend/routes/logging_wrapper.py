import logging
import traceback
from flask import jsonify
from functools import wraps
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, SQLAlchemyError


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except (BadRequest, ValueError, TypeError):
            return jsonify({'error': 'Invalid request'}), 400
        except Unauthorized:
            return jsonify({'error': 'Unathorized. Access Denied'}), 401
        except Forbidden:
            return jsonify({'error': 'You are not allowed to do that.'}), 403

        # Database errors (log only, hide message)
        except (IntegrityError, DataError, OperationalError, SQLAlchemyError) as e:
            logging.error(f"Database Error: {e}\n{traceback.format_exc()}")
            return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

        # Catch-all for anything else
        except Exception as e:
            logging.error(f"Unhandled Error: {e}\n{traceback.format_exc()}")
    return wrapper
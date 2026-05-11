from app.extensions  import db
from flask import Blueprint


follow_bp = Blueprint('follow', __name__, url_prefix='/follow')


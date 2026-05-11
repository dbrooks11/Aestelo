from app.extensions  import db
from flask import Blueprint


block_bp = Blueprint('block', __name__, url_prefix='/block')

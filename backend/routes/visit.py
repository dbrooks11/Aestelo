from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from extensions import db



visit_bp = Blueprint('visit', __name__, url_prefix='/visit')


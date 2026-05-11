from datetime import datetime, timezone

from .extensions import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

visit_bp = Blueprint('visit', __name__, url_prefix='/visit')


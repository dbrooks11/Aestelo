from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from models.followers_and_following import Follow
from models.block_profile import BlockProfile
from routes.auth_required_wrapper import auth_required

block_bp = Blueprint('block', __name__, url_prefix='/block')


@block_bp.route('/<string:username>/block-profile', methods = ['POST'])
@auth_required
def block_profile:
    
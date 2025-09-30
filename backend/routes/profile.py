from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user_profile import UserProfile
from schemas.profile_schema import ProfileSchema
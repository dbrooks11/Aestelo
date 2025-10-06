from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile
from models.followers_and_following import Follow
from routes.auth_required_wrapper import auth_required
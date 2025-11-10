# routes/__init__.py
from .auth import auth_bp
from .profile import profile_bp
from .follow import follow_bp
from .block import block_bp
from .post import post_bp
from .visit import visit_bp
from .user_info import user_info_bp
from .user_settings import user_settings_bp
from .music_track import music_bp

routes = [
    auth_bp,
    profile_bp,
    follow_bp,
    block_bp,
    post_bp,
    visit_bp,
    user_info_bp,
    user_settings_bp,
    music_bp,
]

def register_blueprints(app):
    for route in routes:
        app.register_blueprint(route)
    
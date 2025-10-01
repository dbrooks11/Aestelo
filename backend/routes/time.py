from datetime import datetime, timezone
from flask import Blueprint, jsonify

time_bp = Blueprint('time', __name__, url_prefix ='/api/time')

@time_bp.route('/showtime')
def get_current_time():
    return jsonify({
        'time': datetime.now(timezone.utc).strftime('%b %d, %Y %H:%M:%S')})
import os

import redis
from app.extensions  import db
from flask import Blueprint, current_app, jsonify
from sqlalchemy import text
from utils import s3

health_bp = Blueprint('health', __name__, url_prefix='/health')

@health_bp.route('/health')
def health_check():
    status = {"api": "ok"}

    # --- DB CHECK (Supabase) --- #
    try:
        db.session.execute(text("SELECT 1"))
        status["database"] = "ok"
    except Exception as e:
        status["database"] = str(e)

    # --- REDIS CHECK --- #
    try:
        r = redis.from_url(os.environ["REDIS_URL"])
        r.ping()
        status["redis"] = "ok"
    except Exception as e:
        status["redis"] = str(e)

    # --- CELERY WORKER CHECK --- #
    celery = current_app.extensions["celery"]
    try:
        inspect = celery.control.inspect(timeout=1)
        workers = inspect.ping()
        if workers:
            status["celery"] = list(workers.keys())
        else:
            status["celery"] = "no workers responding"
    except Exception as e:
        status["celery"] = str(e)

    # --- S3 CHECK ---#
    try:
        s3.list_buckets()
        status["r2"] = "ok"
    except Exception as e:
        status["r2"] = str(e)

    healthy = all(v == "ok" or isinstance(v, list) for v in status.values())
    return jsonify(status), (200 if healthy else 500)
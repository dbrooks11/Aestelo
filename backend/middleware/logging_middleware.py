import uuid
from datetime import datetime, timezone

from flask import g, request


def configure_logging_middleware(app):
    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        g.start_time = datetime.now(timezone.utc)

    @app.after_request
    def add_request_id_header(response):
        response.headers['X-Request-ID'] = g.request_id
        return response
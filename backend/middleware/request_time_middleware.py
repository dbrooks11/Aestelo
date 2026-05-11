import time

from flask import g, request


def configure_request_time(app):

    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        if request.path.startswith('/static'): 
            return response
        now = time.time()
        duration = round(now - g.start, 2)
        duration_ms = round((now - g.start) * 1000, 2)
        print(f"REQUEST: {request.method} {request.path} took {duration}s/{duration_ms}ms")
        return response
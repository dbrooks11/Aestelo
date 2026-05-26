import time
import structlog
from litestar.middleware.base import AbstractMiddleware
from litestar.types import Receive, Scope, Send
from app.settings import settings

logger = settings.logger

class RequestTimingMiddleware(AbstractMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.perf_counter()
        status_code = 500

        async def send_wrapper(message: dict) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        await self.app(scope, receive, send_wrapper)

        duration_ms = (time.perf_counter() - start) * 1000
        await logger.ainfo(
            "request completed",
            method=scope["method"],
            path=scope["path"],
            status_code=status_code,
            duration_ms=round(duration_ms, 2),
        )
from collections.abc import AsyncIterator
import pytest
import asyncio
from litestar.testing import AsyncTestClient
from tests.integration.test_auth import TestAuth
from app.middleware.sessions import server_session_config
from app.app import app
from litestar import Litestar


pytestmark = pytest.mark.anyio


@pytest.fixture(scope="class")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app, session_config=server_session_config) as client:
        yield client


@pytest.fixture(scope="class")
async def test_user(test_client: AsyncTestClient[Litestar]):
    res = await test_client.post(
        f"{TestAuth.path}/signup",
        json={
            "email": "test@example.com",
            "password": "test1234",
            "confirm_password": "test1234",
        },
    )

    assert res.status_code == 201
    yield


@pytest.fixture(scope="class")
async def authenticated_client(
    test_client: AsyncTestClient[Litestar],
) -> AsyncTestClient[Litestar]:
    res = await test_client.post(
        f"{TestAuth.path}/login",
        json={"email": "test@example.com", "password": "test1234"},
    )

    assert res.status_code == 201

    csrf_res = await test_client.post(f"{TestAuth.path}/csrf")
    assert csrf_res.status_code == 200

    return test_client


@pytest.fixture
async def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

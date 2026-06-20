import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient


@pytest.mark.anyio
class TestHealth:
    path = "/healthz"

    async def test_health(
        self, authenticated_client: AsyncTestClient[Litestar]
    ) -> None:
        res = await authenticated_client.get(self.path)
        assert res.status_code == 200

    async def test_db(self, authenticated_client: AsyncTestClient[Litestar]) -> None:
        res = await authenticated_client.get(f"{self.path}/db")
        assert res.status_code == 200

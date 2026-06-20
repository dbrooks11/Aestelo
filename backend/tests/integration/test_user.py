import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient


@pytest.mark.anyio
class TestUser:
    path = "/profile"

    async def test_get_profile(self, authenticated_client: AsyncTestClient[Litestar]):
        res = await authenticated_client.get(f"{self.path}")

        assert res.status_code == 200
        assert res.json()

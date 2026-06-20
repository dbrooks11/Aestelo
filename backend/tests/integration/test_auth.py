import pytest
from litestar.testing import AsyncTestClient
from litestar import Litestar

@pytest.mark.anyio
class TestAuth:

    path = '/auth'

    async def test_logout(self, authenticated_client: AsyncTestClient[Litestar]):
        res = await authenticated_client.post(f'{self.path}/sign-out')
        assert res.status_code == 201

    
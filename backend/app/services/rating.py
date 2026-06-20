from app.models import Rating
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from sqlalchemy import select
from litestar.di import NamedDependency


class RatingService(SQLAlchemyAsyncRepositoryService[Rating]):
    class RatingRepo(SQLAlchemyAsyncRepository[Rating]):
        model_type = Rating

    repository_type = RatingRepo

    async def get_rating(self, user_id: str, spot_id: int) -> Rating | None:
        return await self.get_one_or_none(
            statement=select(Rating).where(
                Rating.user_id == user_id, Rating.spot_id == spot_id
            )
        )


async def provide_rate_service(
    db_session: NamedDependency[AsyncSession],
) -> AsyncGenerator[RatingService]:
    async with RatingService.new(session=db_session) as service:
        yield service

from app.models import Spot, SpotMedia, Rating, Visit, CollectionItem
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset, OrderBy, SearchFilter
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from app.schemas.spot import SpotSchemaBase
from litestar.pagination import ClassicPagination
from sqlalchemy import select
from sqlalchemy.orm import with_expression
from math import ceil
from app.db.enums import UploadStatusEnum
from litestar.di import NamedDependency

class SpotService(SQLAlchemyAsyncRepositoryService[Spot]):
    """Handles database operations for spots"""

    class SpotRepo(SQLAlchemyAsyncRepository[Spot]):

        model_type=Spot
    
    repository_type=SpotRepo

    async def get_spots_me_pagination(self, user_id: str, page: int, page_size: int, search_filter: SearchFilter | None = None) -> ClassicPagination[Spot]:  
        visit_subqeury = (select(1).where(Visit.spot_id == Spot.id, Visit.user_id == user_id).exists())
        rated_subquery = (select(1).where(Rating.spot_id == Spot.id, Rating.user_id == user_id).exists())
        saved_subquery = (select(1).where(CollectionItem.spot_id == Spot.id, CollectionItem.saved_by == user_id).exists())

        stmt = select(
                Spot
            ).where(
                Spot.user_id == user_id,
                Spot.status == UploadStatusEnum.SUCCESS
            ).options(
                with_expression(Spot.visited, visit_subqeury),
                with_expression(Spot.rated, rated_subquery),
                with_expression(Spot.saved, saved_subquery)
            )

        filters: list[Any] = [
            LimitOffset(limit=page_size, offset=(page - 1) * page_size),
            OrderBy(field_name='created_at', sort_order='asc')
        ]
        if search_filter:
            filters.append(search_filter)
        items, total = await self.get_many_and_count(*filters, statement=stmt)
        total_pages = ceil(total/page_size) if page_size > 0 else 1
        return ClassicPagination(items=list(items), page_size=total, current_page=page, total_pages=total_pages)
    
    async def create_spot(self, user_id: str, data: SpotSchemaBase) -> Spot:
        model_data = data.model_dump()
        model_data['user_id'] = user_id
        spot = await self.create(data=model_data)
        await self.repository.session.flush()
        await self.repository.session.commit()
        return spot
    
    async def update_spot(self, data, spot_id: int) -> Spot:
        return await self.update(data=data, item_id=spot_id)
    

async def provide_spot_service(db_session: NamedDependency[AsyncSession]) -> AsyncGenerator[SpotService]:
    async with SpotService.new(session=db_session) as service:
        yield service


class SpotMediaService(SQLAlchemyAsyncRepositoryService[SpotMedia]):

    class SpotMediaRepo(SQLAlchemyAsyncRepository[SpotMedia]):

        model_type=SpotMedia

    repository_type=SpotMediaRepo


async def provide_spot_media_service(db_session: NamedDependency[AsyncSession]) -> AsyncGenerator[SpotMediaService]:
    async with SpotMediaService.new(session=db_session) as service:
        yield service
from app.db.models import Spot, SpotMedia
from advanced_alchemy.repository import SQLAlchemyAsyncRepository, ErrorMessages
from advanced_alchemy.filters import LimitOffset, OrderBy, SearchFilter, CollectionFilter
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from typing import Sequence, Literal, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from app.schemas.spot import SpotSchemaBase
from app.schemas.spot import SpotMediaInsert
from litestar.pagination import OffsetPagination


class SpotService(SQLAlchemyAsyncRepositoryService[Spot]):
    """Handles database operations for spots"""

    class SpotRepo(SQLAlchemyAsyncRepository[Spot]):

        model_type=Spot
    
    repository_type=SpotRepo

    async def get_spots_me_pagination(self, user_id: str, page: int, page_size: int, sort_order: Literal['asc','desc'], search_filter: Optional[SearchFilter] = None) -> OffsetPagination[Spot]:  
        offset: int = (page - 1) * page_size
        filters: list[Any] = [
            LimitOffset(limit=page_size, offset=offset),
            OrderBy(field_name='created_at', sort_order=sort_order),
            CollectionFilter(field_name='user_id', values=[user_id])
        ]
        if search_filter:
            filters.append(search_filter)
        items, total = await self.list_and_count(*filters)
        return OffsetPagination(items=items, limit=page_size, offset=offset, total=total)
    
    async def create_spot(self, user_id: str, data: SpotSchemaBase) -> Spot:
        model_data = data.model_dump()
        model_data['user_id'] = user_id
        return await self.create(data=model_data)
    
    async def update_spot(self, data, spot_id: int) -> Spot:
        return await self.update(data=data, item_id=spot_id)
    

async def provide_spot_service(db_session: AsyncSession) -> AsyncGenerator[SpotService, None]:
    async with SpotService.new(session=db_session) as service:
        yield service


class SpotMediaService(SQLAlchemyAsyncRepositoryService[SpotMedia]):

    class SpotMediaRepo(SQLAlchemyAsyncRepository[SpotMedia]):

        model_type=SpotMedia

    repository_type=SpotMediaRepo


async def provide_spot_media_service(db_session: AsyncSession) -> AsyncGenerator[SpotMediaService, None]:
    async with SpotMediaService.new(session=db_session) as service:
        yield service
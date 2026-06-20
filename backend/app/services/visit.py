from app.models import Visit, VisitMedia
from app.schemas.visit import VisitSchemaBase
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset, OrderBy, SearchFilter, CollectionFilter
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from typing import Literal, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from litestar.pagination import OffsetPagination
from litestar.di import NamedDependency

class VisitService(SQLAlchemyAsyncRepositoryService[Visit]):
    """Handles database operations for visits"""

    class VisitRepo(SQLAlchemyAsyncRepository[Visit]):

        model_type=Visit
    
    repository_type=VisitRepo

    async def get_visits_me_pagination(self, user_id: str, page: int, page_size: int, sort_order: Literal['asc','desc'], search_filter: Optional[SearchFilter] = None) -> OffsetPagination[Visit]:  
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
    
    async def create_visit(self, user_id: str, data: VisitSchemaBase) -> Visit:
        model_data = data.model_dump()
        model_data['user_id'] = user_id
        return await self.create(data=model_data)
    
    async def update_visit(self, data, visit_id: int) -> Visit:
        return await self.update(data=data, item_id=visit_id)
    

async def provide_visit_service(db_session: NamedDependency[AsyncSession]) -> AsyncGenerator[VisitService, None]:
    async with VisitService.new(session=db_session) as service:
        yield service


class VisitMediaService(SQLAlchemyAsyncRepositoryService[VisitMedia]):

    class VisitMediaRepo(SQLAlchemyAsyncRepository[VisitMedia]):

        model_type=VisitMedia

    repository_type=VisitMediaRepo


async def provide_visit_media_service(db_session: NamedDependency[AsyncSession]) -> AsyncGenerator[VisitMediaService, None]:
    async with VisitMediaService.new(session=db_session) as service:
        yield service
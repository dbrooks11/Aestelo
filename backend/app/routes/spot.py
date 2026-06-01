from litestar.controller import Controller
from litestar import get, post, Request
from typing import Any
from litestar.di import Provide
from app.db.models.dto.spot import SpotDTO
from app.db.models.services.spot import provide_spot_service, SpotService
from app.db.models.services.rating import RatingService, provide_rate_service
from app.db.models import Spot, Rating
from app.schemas.spot import SpotSchemaBase, SpotInputWithMediaSchema, SpotRatingSchema
from litestar.pagination import ClassicPagination
from litestar.params import FromPath
from app.plugins import plugins
from sqlalchemy import select
from advanced_alchemy.filters import ComparisonFilter

class SpotController(Controller):
    path='/spot'
    dependencies={'spot_service': Provide(provide_spot_service), 'rate_service': Provide(provide_rate_service)}


    @get(return_dto=SpotDTO)
    async def spot_me(self, request: Request, spot_service: SpotService) -> ClassicPagination[Spot]:
        user_id: str = request.user.id
        return await spot_service.get_spots_me_pagination(user_id=user_id, page_size=12, page=1)

    @post(return_dto=SpotDTO)
    async def create_spot(self, data: SpotInputWithMediaSchema, request: Request, spot_service: SpotService) -> Spot:
        user_id: str = request.user.id
        post_type = 'spot'
        model_dump = data.model_dump()

        media: list[str] = model_dump.pop('media')

        spot = await spot_service.create_spot(user_id=user_id, data=SpotSchemaBase.model_validate(model_dump, extra='ignore'))

        tasks = []
        for order, key in enumerate(media, 1):
            tasks.append({'sort_order': order, 'obj_key': key})
        if tasks:
            queue = plugins.saq.get_queue('media_processing')

            await queue.enqueue(
                'process_post_pipeline',
                tasks=tasks,
                post_id=spot.id,
                post_type=post_type,
                user_id=user_id,
                timeout=60,
                retries=2,
                retry_delay=3,
                retry_backoff=True
            )
        return spot
        
    @post('{spot_id:int}/rate')
    async def rate_spot(self, spot_id: FromPath[int], data: SpotRatingSchema, rate_service: RatingService, request: Request) -> int | None:
        user_id: str = request.user.id

        prev_rating = await rate_service.get_rating(user_id=user_id, spot_id=spot_id)

        if prev_rating and data.rating == prev_rating.rating_choice:
            return data.rating


        return prev_rating.rating_choice if prev_rating else None

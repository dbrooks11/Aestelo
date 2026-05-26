from litestar.controller import Controller
from litestar import get, post, delete, patch, Request
from litestar.di import Provide
from typing import Sequence
from app.db.models.dto.spot import SpotDTO
from app.db.models.services.spot import provide_spot_service, SpotService
from app.db.models.spot import Spot, SpotMedia
from app.schemas.spot import SpotSchemaBase, SpotInputWithMediaSchema
from litestar.pagination import OffsetPagination
from app.plugins import plugins
from geoalchemy2.functions import ST_Point
from app.utils.storage import storage_bb


class SpotController(Controller):
    path='/spot'
    dependencies={'spot_service': Provide(provide_spot_service)}


    @get(return_dto=SpotDTO)
    async def spot_me(self, request: Request, spot_service: SpotService) -> OffsetPagination[Spot]:
        user_id = request.user.id
        return await spot_service.get_spots_me_pagination(user_id=user_id, page_size=12, page=1, sort_order='asc')

    @post(return_dto=SpotDTO)
    async def create_spot(self, data: SpotInputWithMediaSchema, request: Request, spot_service: SpotService) -> Spot:
        user_id=request.user.id
        model_dump = data.model_dump()


        media: list[str] = model_dump.pop('media')

        spot = await spot_service.create_spot(user_id=user_id, data=SpotSchemaBase.model_validate(model_dump, extra='ignore'))
        
        queue = plugins.saq.get_queue('media_processing')

        tasks = []
        for order, key in enumerate(media, 1):
                tasks.append({'post_type': 'spot', 'post_id': spot.id, 'sort_order': order, 'obj_key': key})

        media_data: list[dict[str, int | str]] = []
        async with queue.batch():
            try:
                media_data = await queue.map(
                    '',
                    tasks,
                    timeout=120,
                    poll_interval=1.0,
                    retries=3,
                    retry_delay=1,
                    retry_backoff=True
                )
                # if len(media_data) != len(media):
                #     raise Exception('Failed to create Spot')
                result: dict[str, int] = await queue.apply(
                    '',
                    data=media_data,
                    user_id=user_id,
                    post_id=spot.id,
                    post_type='spot',
                    timeout=60,
                    poll_interval=1.0,
                    retries=3,
                    retry_delay=2,
                    retry_backoff=True
                )
            except Exception:
                for item in media_data:
                    key: str = item.get('media_key') # type: ignore[attr-defined]
                    await storage_bb.delete_file_s3(key)
                raise
            coordinates = ST_Point(result.get('long'), result.get('lat'))
        return await spot_service.update_spot(data={'coordinates': coordinates}, spot_id=spot.id)
            

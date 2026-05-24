import pyvips
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from app.utils.storage import ObjectStorage
from app.settings import settings


MAX_DIMENSION = 2048
QUALITY = 85
COMPRESSION_IMAGE_TYPE='webp'

media_executioner = ThreadPoolExecutor(thread_name_prefix='media', max_workers=settings.app.CPU_COUNT)


async def process_media_image(storage: ObjectStorage, obj_key: str, need_exif: bool) -> dict[Any, Any]:
    buffer = await storage.get_object_s3(key=obj_key)
    
    loop = asyncio.get_running_loop()
    def process_in_thread():
        image = pyvips.Image.thumbnail_buffer(
            buffer,
            MAX_DIMENSION,
            height=MAX_DIMENSION,
            size=pyvips.enums.Size.DOWN,
        )  # type: ignore[attr-defined]
        exif = image.get_fields() if need_exif else None   # type: ignore[attr-defined]   
        print(f'THIS IS EXIF DATA: {exif}')
        new_image = image.write_to_buffer(f'.{COMPRESSION_IMAGE_TYPE}', Q=85, keep=pyvips.enums.ForeignKeep.ICC)  # type: ignore[attr-defined]

        return {'compressed_file': new_image, 'exif': exif, 'mimetype': f'image/{COMPRESSION_IMAGE_TYPE}'}
    
    
    compressed_data = await loop.run_in_executor(media_executioner, process_in_thread)
    print(compressed_data)
    return compressed_data
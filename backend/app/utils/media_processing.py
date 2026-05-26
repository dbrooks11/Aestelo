import pyvips
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from app.utils.storage import ObjectStorage
from app.settings import settings
from app.lib.validation import validate
from modern_colorthief import get_color, get_palette

media_executioner = ThreadPoolExecutor(thread_name_prefix='media', max_workers=settings.app.CPU_COUNT)


async def process_media_image(storage: ObjectStorage, obj_key: str, need_exif: bool, need_colors: bool) -> dict[Any, Any]:
    buffer = await storage.get_object_s3(key=obj_key)

    if len(buffer) > validate.MAX_FILE_SIZE:
        raise Exception(f'File exceeds {validate.MAX_FILE_SIZE} limit')
    
    loop = asyncio.get_running_loop()
    def process_in_thread():
        image = pyvips.Image.thumbnail_buffer(
            buffer,
            validate.MAX_WIDTH,
            height=validate.MAX_HEIGHT,
            size=pyvips.enums.Size.DOWN,
        )  # type: ignore[attr-defined]
        exif: list = image.get_fields() if need_exif else None  # type: ignore[attr-defined] 
        new_image = image.write_to_buffer(f'.{validate.COMPRESSION_IMAGE_TYPE}', Q=85, keep=pyvips.enums.ForeignKeep.ICC)  # type: ignore[attr-defined]
        color_palette = get_palette(new_image, color_count=8, quality=10) if need_colors else None

        return {'compressed_file': new_image, 
                'exif': exif, 
                'mimetype': f'image/{validate.COMPRESSION_IMAGE_TYPE}',
                'color_palette': color_palette}
    
    
    compressed_data = await loop.run_in_executor(media_executioner, process_in_thread)
    return compressed_data
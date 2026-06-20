import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pyvips

from app.lib.validation import validate
from app.settings import settings
from app.utils.storage import ObjectStorage

pyvips.cache_set_max(0)
pyvips.cache_set_max_mem(0)
pyvips.cache_set_max_files(0)

media_executioner = ThreadPoolExecutor(
    thread_name_prefix="media", max_workers=settings.misc.MAX_CONCURRENT_IMAGES
)


async def process_media_image(
    storage: ObjectStorage, obj_key: str, need_exif: bool, need_colors: bool
) -> dict[Any, Any]:
    try:
        body, file_size = await storage.get_object_s3_stream(key=obj_key)
        if file_size > validate.MAX_FILE_SIZE:
            raise Exception(f"File exceeds {validate.MAX_FILE_SIZE} limit")

        loop = asyncio.get_running_loop()

        def process_in_thread(raw_bytes: bytes):
            image = None
            try:
                image = pyvips.Image.thumbnail_buffer(
                    raw_bytes,
                    validate.MAX_WIDTH,
                    height=validate.MAX_HEIGHT,
                    size=pyvips.enums.Size.DOWN,
                )  # type: ignore[attr-defined]
                tags = ["GPS"]
                exif: list = image.get_fields() if need_exif else None  # type: ignore[attr-defined]
                exif_dict: dict = {}
                if exif:
                    loader: str = image.get("vips-loader")  # type: ignore[attr-defined]
                    original_filetype: str = loader.split("load")[0] if loader else None  # type: ignore[attr-defined]
                    for field in exif:
                        if any(tag.lower() in field.lower() for tag in tags):
                            exif_dict[field] = image.get(field)  # type: ignore[attr-defined]
                new_image = image.write_to_buffer(
                    f".{validate.COMPRESSION_IMAGE_TYPE}",
                    Q=85,
                    keep=pyvips.enums.ForeignKeep.ICC,
                )  # type: ignore[attr-defined]

                return {
                    "compressed_file": new_image,
                    "exif": exif_dict,
                    "original_mimetype": f"image/{original_filetype}",
                    "new_mimetype": f"image/{validate.COMPRESSION_IMAGE_TYPE}",
                }
            finally:
                if image:
                    image = None

        compressed_data = await loop.run_in_executor(
            media_executioner, process_in_thread, body
        )
        return compressed_data
    except:
        raise

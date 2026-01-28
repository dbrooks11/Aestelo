from PIL import ExifTags, ImageOps, Image, ImageFile
from PIL.Image import DecompressionBombError
from pillow_heif import register_heif_opener
import io
from tempfile import NamedTemporaryFile
from flask import current_app


register_heif_opener()
ALLOWED_FORMATS = ('JPEG', 'PNG', 'HEIF', 'HEIC')
Image.MAX_IMAGE_PIXELS = 100_000_000
ImageFile.LOAD_TRUNCATED_IMAGES = True


def get_decimal_coordinates(gps_info, key):
    
    if not gps_info:
        return None, None

    def to_float(value):
        try:
            if isinstance(value, (int, float)):
                return float(value)
            
            if isinstance(value, (tuple, list)) and len(value) == 2:
                if value[1] == 0: 
                    return 0.0
                return float(value[0]) / float(value[1])
            
            if hasattr(value, 'numerator') and hasattr(value, 'denominator'):
                if value.denominator == 0: 
                    return 0.0
                return float(value.numerator) / float(value.denominator)
                
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def dms_to_decimal(dms, ref):
        try:
            degrees = to_float(dms[0])
            minutes = to_float(dms[1])
            seconds = to_float(dms[2])

            decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

            if ref in ['S', 'W']:
                decimal = -decimal
            
            return float(f'{decimal:.6f}')
        except Exception:
            return None, None

    try:
        photo_lat = gps_info.get(2)
        photo_lat_ref = gps_info.get(1)
        photo_long = gps_info.get(4)
        photo_long_ref = gps_info.get(3)

        if not photo_lat or not photo_long:
            raise Exception('Invalid GPS metadata')

        latitude = dms_to_decimal(photo_lat, photo_lat_ref)
        longitude = dms_to_decimal(photo_long, photo_long_ref)

        if (latitude is None or longitude is None) or (latitude == 0.0 and longitude == 0.0):
            raise Exception('Invalid GPS metadata')

        return latitude, longitude

    except Exception:
        return None, None


def photo_processing_one_img_metadata(file_path: str, current_user_id: str):
    try:
        with Image.open(file_path) as img:
            try:
                img.verify()
            except Exception:
                raise Exception("Corrupt image file integrity check failed.")
            
        with Image.open(file_path) as img:

            if img.format not in ALLOWED_FORMATS:
                raise Exception(f"Unsupported format: {img.format}")
        
            img = ImageOps.exif_transpose(img)

            if img.mode not in ['RGB', 'RGBA', 'P']:
                img = img.convert('RGBA')
            
            exif = img.getexif()
            if exif:
                gps = exif.get_ifd(ExifTags.IFD.GPSInfo)

            # TODO: handle user chosen aspect size instead
            max_width, max_height = 1080, 1350
            if img.width > max_width or img.height > max_height:
                img.thumbnail(size=(max_width, max_height), resample=Image.Resampling.LANCZOS)
            
            file_type = "WEBP"
            output = file_path + f'processed_{file_type.lower()}'
            img.save(output, 
                    format=file_type, 
                    quality=85, 
                    method=6, 
                    exif= b'', 
                    subsampling=0,
                    lossless=False
                    )
            return {
                'file_path': output,
                'gps': gps,
                'width': img.size[0],
                'height': img.size[1],
                'type': 'photo'
            }
    except DecompressionBombError:
        current_app.logger.warning(f"User {current_user_id} attempted Decompression Bomb upload.")
        raise DecompressionBombError("Image is too large or complex.")
    except OSError:
        raise OSError(f"photo {file_path}: could not be opened")
    except Exception as e:
            raise Exception(f"photo {file_path}: Failed to process - {str(e)}")


    

# TODO: raise errors instead of returning them and use SSD instead of ram
def photo_processing_one_img(img_file, is_banner: bool, current_user_id: str):

    error = []
    try:
        img = Image.open(img_file)

        if img.format not in ALLOWED_FORMATS:
            error.append(f"Invalid format: {img.format}. Must be JPEG, PNG, HEIC, or HEIF")
            return error
    
        img.verify()
        img = Image.open(img_file)  

    except DecompressionBombError:
        current_app.logger.warning(f"User {current_user_id} attempted Decompression Bomb upload.")
        error.append("Image is too large or complex.")
        return error
    
    except Exception:
        error.append('Invalid Image')
        return error
    
    img = ImageOps.exif_transpose(img)

    if img.mode not in ['RGB', 'RGBA']:
        img = img.convert('RGB')

    if is_banner:
        max_width = 2560
        max_height = 1440
        quality = 90
        if img.width > max_width or img.height > max_height:
            img.thumbnail(size=(max_width, max_height), resample=Image.Resampling.LANCZOS)
    
    if is_banner is False:
        max_width = 500
        max_height = 500
        quality = 80
        if img.width > max_width or img.height > max_height:
            img.thumbnail(size=(max_width, max_height), resample=Image.Resampling.LANCZOS)
        
    output = io.BytesIO()
    img.save(output, format="WEBP", quality=quality, method=6, exif= b'', subsampling=0)
    output.seek(0)
    return output
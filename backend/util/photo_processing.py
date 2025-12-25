from PIL import ExifTags, ImageOps, Image
from PIL.Image import DecompressionBombError
import io
from flask import current_app


#TODO: Put name for compressed files. Use users ID from route and a label (profile photo, banner, etc)



def get_decimal_coordinates(gps_info):

    def dms_to_decimal(dms,ref):
        degrees, minutes, seconds = dms
        decimal = float(degrees + (minutes / 60) + (seconds / 3600))

        if ref in ['S','W']:
            decimal = -decimal

        return float(f'{decimal:.6f}')
    
    def get_altitude(alt_meters, alt_ref):
        if alt_ref == 1:
            alt_meters = -alt_meters

        return float(alt_meters)
    

    photo_lat = gps_info.get(2)
    photo_lat_ref = gps_info.get(1)
    
    photo_long = gps_info.get(4)
    photo_long_ref = gps_info.get(3)

    photo_alt = gps_info.get(6)
    photo_alt_ref = gps_info.get(5)

    latitude, longitude, altitude = None, None, None
    
    if photo_lat and photo_long:
        latitude = dms_to_decimal(photo_lat, photo_lat_ref)
        longitude = dms_to_decimal(photo_long, photo_long_ref)
        
        if photo_alt:
            altitude = get_altitude(photo_alt,photo_alt_ref)
            return latitude, longitude, altitude
        return latitude, longitude, None

    return latitude,longitude,altitude




def photo_processing(*photos: tuple):
    min_width = 500
    max_width = 1080 
    min_height = 500 
    max_height = 1350

    if not photos:
        return {'error': 'No photos provided'}, 400
    
    processed_photos = []
    errors = []
    pht_count = 0
    
    for photo in photos:
        pht_count += 1
        try:
            im = Image.open(io.BytesIO(photo))
            
            # Check format
            if im.format not in ['JPEG', 'PNG', 'HEIF']:
                errors.append(f"photo {pht_count}: Invalid format '{im.format}'. Must be JPEG, PNG, or HEIF")
                continue

            exif = im.getexif()
            gps = exif.get_ifd(ExifTags.IFD.GPSInfo)
            im = ImageOps.exif_transpose(im)

            width, height = im.size
            if width < min_width or height < min_height:
                errors.append(f'photo {pht_count} is too small: {width}x{height}')
                continue

            if width > max_width or height > max_height:
                im.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            # Check color mode
            if im.mode not in ['RGB']:
                if im.mode == 'RGBA':
                    background = Image.new('RGB', im.size, (255,255,255))
                    background.paste(im, mask=im.split()[3])
                    im = background
                else:
                    errors.append(f"photo {pht_count}: Invalid mode '{im.mode}'. Must be RGB or RGBA")
                    continue


            thumbnail = im.copy()
            thumbnail.thumbnail((550,550), Image.Resampling.LANCZOS)

            output = io.BytesIO()
            im.save(output, format='JPEG', quality = 90, exif = b'')
            output.seek(0)

            thumbnail_output = io.BytesIO()
            thumbnail.save(thumbnail_output, format='JPEG', quality = 85, exif = b'')
            thumbnail_output.seek(0)
            
            processed_photos.append({
                'photo_num': pht_count,
                'photo': output,
                'thumbnail':thumbnail_output,
                'exif': exif,
                'gps': gps,
                'width': im.size[0],
                'height': im.size[1],
                'is_primary': False,
                'photo_type': 'photo' if im.format in ['JPEG', 'PNG', 'HEIF'] else None
            })
        
        except OSError:
            errors.append(f"photo {pht_count}: could not be opened")
        except Exception as e:
            errors.append(f"photo {pht_count}: Failed to process - {str(e)}")
    
    if errors:
        return {
            'error': 'photo validation failed',
            'details': errors
        }, 422
    
    return {
        'message': 'All photos processed successfully',
        'photos': processed_photos
    }, 200
    



def photo_processing_one_img(img_file, is_banner: bool, current_user_id: str):

    error = []
    try:
        img = Image.open(img_file)

        if img.format not in ('JPEG', 'PNG', 'HEIF'):
            error.append(f"Invalid format: {img.format}. Must be JPEG, PNG, or HEIF")
            return error
    
    
        img.verify()

    except DecompressionBombError:
        current_app.logger.warning(f"User {current_user_id} attempted Decompression Bomb upload.")
        error.append("Image is too large or complex.")
        return error
    
    except Exception:
        error.append('Invalid Image')
        return error

    if img.mode not in ['RGB', 'RGBA']:
        img = img.convert('RGB')

    if is_banner:
        max_width = 1920
        max_height = 1080

        if img.width > max_width or img.height > max_height:
            img = img.thumbnail(size=(max_width, max_height), resample=Image.Resampling.LANCZOS)

    
    if is_banner is False:
        max_width = 500
        max_height = 500

        if img.width > max_width or img.height > max_height:
            img = img.thumbnail(size=(max_width, max_height), resample=Image.Resampling.LANCZOS)
        
    output = io.BytesIO()
    img.save(output, format="WEBP", quality=90, method=6, exif= b'')
    output.seek(0)
    return output
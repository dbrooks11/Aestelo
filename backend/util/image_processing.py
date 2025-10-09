from PIL import Image, ImageOps, ImageFilter, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import os, sys
import io
from urllib.request import urlopen
from flask import jsonify


def get_decimal_coordinates(gps_info):

    def dms_to_decimal(dms,ref):
        degrees, minutes, seconds = dms
        decimal = float(degrees + (minutes / 60) + (seconds / 3600))

        if ref in ['S','W']:
            decimal = -decimal

        return f'{decimal:.6f}'
    
    def get_altitude(alt_meters, alt_ref):
        if alt_ref == 1:
            alt_meters = -alt_meters

        return alt_meters
    

    image_lat = gps_info.get(2)
    image_lat_ref = gps_info.get(1)
    
    image_long = gps_info.get(4)
    image_long_ref = gps_info.get(3)

    image_alt = gps_info.get(6)
    image_alt_ref = gps_info.get(5)

    
    if image_lat and image_long:
        latitude = dms_to_decimal(image_lat, image_lat_ref)
        longitude = dms_to_decimal(image_long, image_long_ref)
        
        if image_alt:
            altitude = get_altitude(image_alt,image_alt_ref)
            return latitude, longitude, altitude
        return latitude, longitude, None

    return None, None, None


def image_processing(*images):
    min_width = 600
    max_width = 1080 
    min_height = 600 
    max_height = 1350

    if not images:
        return {'error': 'No images provided'}, 400
    
    processed_images = []
    errors = []
    img_count = 0
    
    for image in images:
        img_count += 1
        try:
            im = Image.open(io.BytesIO(image))
            
            # Check format
            if im.format not in ['JPEG', 'PNG', 'HEIF']:
                errors.append(f"Image {img_count}: Invalid format '{im.format}'. Must be JPEG, PNG, or HEIF")
                continue

            exif = im.getexif()
            gps = exif.get_ifd(ExifTags.IFD.GPSInfo)
            im = ImageOps.exif_transpose(im)

            width, height = im.size
            if width < min_width or height < min_height:
                errors.append(f'Image {img_count} is too small: {width}x{height}')
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
                    errors.append(f"Image {img_count}: Invalid mode '{im.mode}'. Must be RGB or RGBA")
                    continue


            thumbnail = im.copy()
            thumbnail.thumbnail((600,600), Image.Resampling.LANCZOS)

            output = io.BytesIO()
            im.save(output, format='JPEG', quality = 85, optimize = True, exif = b'')
            output.seek(0)

            thumbnail_output = io.BytesIO()
            thumbnail.save(thumbnail_output, format='JPEG', quality = 90, optimize = True, exif = b'')
            thumbnail_output.seek(0)
            
            processed_images.append({
                'image_num': img_count,
                'image': output,
                'thumbnail':thumbnail_output,
                'exif': exif,
                'gps': gps,
                'width': im.size[0],
                'height': im.size[1],
                'is_primary': False,
                'media_type': 'image',
            })
        
        except OSError:
            errors.append(f"Image {img_count}: could not be opened")
        except Exception as e:
            errors.append(f"Image {img_count}: Failed to process - {str(e)}")
    
    if errors:
        return {
            'error': 'Image validation failed',
            'details': errors
        }, 422
    
    return {
        'message': 'All images processed successfully',
        'images': processed_images
    }, 200
    
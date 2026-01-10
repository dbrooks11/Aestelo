import boto3
from botocore.client import Config, ClientError
from flask import current_app
from datetime import datetime, timezone
import secrets
import os

s3 = boto3.client(
        service_name="s3",
        endpoint_url=os.environ.get('R2_ENDPOINT_URL'),
        aws_access_key_id=os.environ.get('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('R2_SECRET_ACCESS_KEY'),
        region_name='auto',
        config=Config(signature_version='s3v4')
        )

def generate_presigned_url(filename: str, filetype: str, user_id: str, folder: str):
   
    raw_filename_key = temporary_file_path_presigned(user_id=user_id, folder=folder, filename=filename)

    try:
        response = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': current_app.config['R2_BUCKET_NAME'],
                'Key':raw_filename_key,
                'ContentType': filetype
            },
            ExpiresIn=1800
        )

        return {'key': raw_filename_key, 'presigned_url': response } 
    except Exception as e:
        raise Exception(str(e))

         


def temporary_file_path_presigned(user_id: str, folder: str, filename: str):
    timestamp = datetime.now(timezone.utc).strftime('%d%m%Y_%H%M%S')
    short_id = secrets.token_urlsafe(16) 
    unique_filename = f"{folder}/{user_id}/{timestamp}_{short_id}_{filename}"

    return unique_filename

def download_file(file_name: str):
    try:
        response = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': current_app.config['R2_BUCKET_NAME'],
                'Key': file_name
            },
            ExpiresIn=3600
        )

        return response 
    except Exception as e:
        raise Exception(str(e))


def upload_to_r2(file_obj, user_id: str, folder: str):

    bucket = current_app.config['R2_BUCKET_NAME']
    
    try:
        timestamp = datetime.now(timezone.utc).strftime('%d%m%Y_%H%M%S')
        short_id = secrets.token_urlsafe(16) 
        unique_filename = f"{folder}/{user_id}/{timestamp}_{short_id}.webp"
    
        file_obj.seek(0)
        
        s3.upload_fileobj(
            file_obj,
            bucket,
            unique_filename,
            ExtraArgs={
                "ContentType": 'image/webp'
            }
        )
        
        return unique_filename
        
    except ClientError as ce:
        current_app.logger.error(f"R2 Upload Failed: {ce}")
        raise ClientError(f"An error occurred: {ce}")
    except Exception as e:
        raise Exception(f"Upload failed: {e}")
    


def delete_file_r2(file_path):
    bucket = current_app.config['R2_BUCKET_NAME']

    try:
        s3.delete_object(Bucket=bucket, Key=file_path)
        return True
    except ClientError as ce:
        current_app.logger.error(f"R2 Deletion Failed: {ce}")
        return False
    except Exception as e:
        current_app.logger.error(f"R2 Deletion Failed: {e}")
        return False

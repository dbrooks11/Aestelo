import os
import secrets
from datetime import datetime, timezone

import boto3
from botocore.client import ClientError, Config
from flask import current_app

s3 = boto3.client(
        service_name="s3",
        endpoint_url=os.environ.get('R2_ENDPOINT_URL'),
        aws_access_key_id=os.environ.get('R2_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('R2_SECRET_ACCESS_KEY'),
        region_name='auto',
        config=Config(signature_version='s3v4')
        )

def generate_presigned_url(filename: str, filetype: str, user_id: str, folder: str, expires_in: int):
   
    raw_filename_key = temporary_file_path_presigned(user_id=user_id, folder=folder, filename=filename)

    try:
        response = s3.generate_presigned_url(
            'put_object',
            Params = {
                'Bucket': current_app.config['R2_BUCKET_NAME'],
                'Key':raw_filename_key,
                'ContentType': filetype
            },
            ExpiresIn = expires_in if expires_in else 3600
        )

        return {'key': raw_filename_key, 'presigned_url': response } 
    except Exception as e:
        raise Exception(str(e))

         


def temporary_file_path_presigned(user_id: str, folder: str, filename: str):
    timestamp = datetime.now(timezone.utc).strftime('%d%m%Y_%H%M%S')
    short_id = secrets.token_urlsafe(16) 
    unique_filename = f"{folder}/{user_id}/{timestamp}_{short_id}_{filename}"

    return unique_filename


def download_file_from_s3(key: str, local_path: str) -> str:
    bucket = os.environ.get('R2_BUCKET_NAME')
    
    try:
        s3.download_file(
            Bucket=bucket, 
            Key=key, 
            Filename=local_path
        )
    except Exception as e:
        if os.path.exists(local_path):
            os.remove(local_path)
        raise Exception(f"Download failed for {key}: {str(e)}")


def upload_to_s3(file, folder: str):

    bucket = current_app.config['R2_BUCKET_NAME']
    
    try:
        timestamp = datetime.now(timezone.utc).strftime('%d%m%Y_%H%M%S')
        short_id = secrets.token_urlsafe(16) 
        unique_filename = f"{folder}/{timestamp}_{short_id}.webp"
        
        s3.upload_file(
            file,
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
    


def delete_file_s3(file_path: str):
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

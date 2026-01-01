import boto3
from botocore.client import Config, ClientError
from flask import current_app
from datetime import datetime, timezone
import secrets

s3_client = boto3.client(
        's3',
        endpoint_url=current_app.config['R2_ENDPOINT_URL'],
        aws_access_key_id=current_app.config['R2_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['R2_SECRET_ACCESS_KEY'],
        region_name='auto',
        config=Config(signature_version='s3v4')
        )



def upload_to_r2(file_obj, user_id: str, folder: str):

    bucket = current_app.config['R2_BUCKET_NAME']
    
    try:
        timestamp = datetime.now(timezone.utc).strftime('%d%m%Y_%H%M%S')
        short_id = secrets.token_urlsafe(16) 
        unique_filename = f"{folder}/{user_id}/{timestamp}_{short_id}.webp"
    
        file_obj.seek(0)
        
        s3_client.upload_fileobj(
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
        s3_client.delete_object(Bucket=bucket, Key=file_path)
        return True
    except ClientError as ce:
        current_app.logger.error(f"R2 Deletion Failed: {ce}")
        return False
    except Exception as e:
        current_app.logger.error(f"R2 Deletion Failed: {e}")
        return False

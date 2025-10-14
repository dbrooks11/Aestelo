import boto3
from botocore.client import Config, ClientError
from flask import current_app
from datetime import datetime, timezone
import secrets

def get_r2_client():
    return boto3.client(
        's3',
        endpoint_url=current_app.config['R2_ENDPOINT_URL'],
        aws_access_key_id=current_app.config['R2_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['R2_SECRET_ACCESS_KEY'],
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
        )



def upload_to_r2(file_obj, user_id, folder='posts', bucket = None):

    bucket = current_app.config['R2_BUCKET_NAME']
    
    try:
        timestamp = datetime.now(timezone.utc).strftime('%d%m%Y_%H%M%S')
        short_id = secrets.token_urlsafe(16) 
        unique_filename = f"{folder}/{user_id}/{timestamp}_{short_id}.jpg"
    
        s3_client = get_r2_client()
        
        file_obj.seek(0)
        
        # Upload
        s3_client.upload_to_r2(
            file_obj,
            bucket,
            unique_filename,
            ExtraArgs={
                'CacheControl': 'public, max-age=15768000'
            }
        )
       
        public_url = f"{current_app.config['R2_PUBLIC_URL']}/{unique_filename}"
        
        return public_url
        
    except ClientError as e:
        raise ClientError(f"An error occurred: {e}")
    except Exception as e:
        raise Exception(f"R2 upload failed: {str(e)}")
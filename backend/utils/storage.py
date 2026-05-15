
import secrets
from datetime import datetime, timezone
from typing import Literal

import boto3
from utils.exceptions import InvalidFileTypeError, InvalidObjectStorageDestinationError, InvalidConfigurationError
from app.config import Config as appConfig
from botocore.client import ClientError, Config
from flask import current_app


def verify_file_type(mimetype: str):
    """Verifies the file type that is allowed within the app's config"""
    extension: str | None = appConfig.ALLOWED_MIME_TYPES.get(mimetype, None)
    if not extension:
        raise InvalidFileTypeError(mimetype)
    return extension

class ObjectStorage:
    """
    Client wrapper for Cloudflare R2/S3 object storage operations.
    
    Handles presigned URL generation, file uploads/downloads, and file deletions
    for quarantine and processed images. Uses boto3 client configured for R2.
    """
    def __init__(self, 
                 bucket: str | None = appConfig.R2_BUCKET_NAME, 
                 endpoint: str | None = appConfig.R2_ENDPOINT,
                 access_key_id: str | None = appConfig.R2_ACCESS_KEY_ID,
                 secret_access_key: str | None = appConfig.R2_SECRET_ACCESS_KEY,
                 region: str = 'auto'
                 ):
        component = "ObjectStorage Class"
        if not bucket:
            raise InvalidConfigurationError(component=component, missing_field='bucket')
        if not endpoint:
            raise InvalidConfigurationError(component=component, missing_field='endpoint')
        if not access_key_id:
            raise InvalidConfigurationError(component=component, missing_field='access_key_id')
        if not secret_access_key:
            raise InvalidConfigurationError(component=component, missing_field='secret_access_key')
        
        self.bucket = bucket
        self.s3 = boto3.client(
            service_name="s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region,
            config=Config(signature_version='s3v4')
        )

    def temporary_file_path(self, user_id: str, folder: str, mimetype: str):
        """Generate unique file path for S3/R2"""

        extension = verify_file_type(mimetype)
        timestamp = datetime.now(timezone.utc).strftime('%d%m%Y_%H%M%S')
        short_id = secrets.token_urlsafe(32) 
        unique_filename = f"{folder}/{user_id}/{timestamp}_{short_id}.{extension}"

        return unique_filename


    def generate_presigned_url(self, mimetype: str, user_id: str, content_target: Literal['spot','visit','profile'], expires_in: int = 3600):
        """Generate presigned URL"""
        folders = {
            "spot": "quarantine/spot",
            "visit": "quarantine/visit",
            "profile": "quarantine/profile"
        }

        if content_target not in folders:
            raise InvalidObjectStorageDestinationError(folder=content_target)

        folder = folders[content_target]

        object_key = self.temporary_file_path(user_id=user_id, folder=folder, mimetype=mimetype)
        try:
            print(f'Content type file: {mimetype}')

            response = self.s3.generate_presigned_url(
                'put_object',
                Params = {
                    'Bucket': self.bucket,
                    'Key':object_key,
                    'ContentType': mimetype
                },
                ExpiresIn = expires_in
            )

            return {'key': object_key, 'presigned_url': response } 
        except Exception as e:
            raise Exception(f"S3 presigned URL generation failed: {str(e)}")
         

    def download_file_from_s3(self, key: str, local_path: str):   
        """Download file from S3"""
        try:
            self.s3.download_file(
                Bucket=self.bucket, 
                Key=key, 
                Filename=local_path
            )
        except Exception as e:
            raise Exception(f"Download failed for {key}: {str(e)}")

    def head_object_from_s3(self, key: str):
        return self.s3.head_object(Bucket=self.bucket, Key=key)

    def upload_to_s3(self, file, mime_type: str,  user_id: str, content_target: Literal['spot','visit','profile_banner', 'profile_photo']):   
        """Upload a file to S3"""
        folders = {
            "spot": "spot",
            "visit": "visit",
            "profile_photo": "profile_photo",
            "profile_banner": "profile_banner"
        }

        if content_target not in folders:
            raise InvalidObjectStorageDestinationError(content_target)
        
        folder = folders[content_target]

        unique_filename = self.temporary_file_path(user_id=user_id, folder=folder, mimetype=mime_type)
        try:
            self.s3.upload_file(
                file,
                self.bucket,
                unique_filename,
                ExtraArgs={
                    "ContentType": mime_type
                }
            )
            
            return unique_filename  
        except ClientError as ce:
            current_app.logger.error(f"R2 Upload Failed: {str(ce)}")
            raise ClientError(f"An error occurred: {str(ce)}", 'Uploading to s3')
        except Exception as e:
            current_app.logger.error(f"R2 Upload Failed: {str(e)}")
            raise Exception(f"Upload failed: {str(e)}")
        


    def delete_file_s3(self, file_path: str):
        """Delete file from S3"""
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=file_path)
            return True
        except ClientError as ce:
            current_app.logger.error(f"R2 Deletion Failed: {ce}")
            return False
        except Exception as e:
            current_app.logger.error(f"R2 Deletion Failed: {e}")
            return False

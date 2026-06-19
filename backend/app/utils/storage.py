
import secrets
from datetime import datetime, timezone
from typing import Any
from litestar.exceptions import ValidationException
from aioboto3 import Session
from aiobotocore.config import AioConfig
from app.settings import settings


ALLOWED_POST_MIME_TYPES = {
        'image/jpeg': 'jpg',
        'image/jpg': 'jpg',
        'image/heic': 'heic',
        'image/heif': 'heif',
    }

ALLOWED_MIME_TYPES = {
    'image/jpeg': 'jpg',
    'image/jpg': 'jpg',
    'image/png': 'png',
    'image/webp': 'webp',
    'image/heic': 'heic',
    'image/heif': 'heif',
}




class ObjectStorage:
    """
    Client wrapper for S3 object storage operations.
    
    Handles presigned URL generation, file uploads/downloads, and file deletions.
    
    Uses aioboto3 client configured for S3.
    """
    allowed_folders: list[str] = ['spot', 'visit', 'avatar', 'banner','quarantine']
    
    def __init__(self,
                 bucket: str, 
                 endpoint: str,
                 access_key_id: str,
                 secret_access_key: str,
                 region: str = 'auto',
                 service_name: str = 's3'
                 ):
            self.service_name =service_name
            self.endpoint_url = endpoint
            self.access_key_id = access_key_id
            self.secret_access_key = secret_access_key
            self.bucket = bucket
            self.region = region
            self.session = Session()

    async def verify_file_type(self, mimetype: str | None, is_post: bool):
        """Verifies the file type that is allowed"""
        if not mimetype:
            raise ValidationException("Invalid file type: None")
        extension: str | None = ALLOWED_MIME_TYPES.get(mimetype, None) if not is_post else ALLOWED_POST_MIME_TYPES.get(mimetype, None)
        if not extension:
            raise ValidationException(f"Invalid file type {mimetype}")
        return extension

    async def generate_file_name(self, id: str | int, extension: str, folder: str = 'quarantine') -> str:
        """Generate unique file path for the object.
        
        Non-quarantine folder structure:
            {foldername}/{id}/{timestamp}_{short_id}.{extension}

        set is_post=True to validate a specific set of mimetypes for Post like content.

        Allowed Folders: spot, visit, avatar, banner, quarantine
        """

        if folder not in self.allowed_folders:
            raise Exception('Invalid destination') 
        
        timestamp = datetime.now(timezone.utc).strftime('%d%m%Y_%H%M%S')
        short_id = secrets.token_urlsafe(32) 
        filename = f"{folder}/{id}/{timestamp}_{short_id}.{extension}"

        return filename

    async def generate_presigned_put_url(self, mimetype: str, obj_key: str, expires_in: int = 600) -> dict[str, str]:
        """Generate presigned URL"""

        async with self.session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            config=AioConfig(signature_version='s3v4')
        ) as s3: # type: ignore[attr-defined]
            response = await s3.generate_presigned_url(
                'put_object',
                Params = {
                    'Bucket': self.bucket,
                    'Key':obj_key,
                    'ContentType': mimetype
                },
                ExpiresIn = expires_in
            )

        return {'key': obj_key, 'presigned_url': response } 
    
    async def generate_presigned_get_url(self, key: str, expires_in: int = 300) -> str:
        async with self.session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            config=AioConfig(signature_version='s3v4')
        ) as s3: # type: ignore[attr-defined] 
            return await s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expires_in,
            )
         

    async def download_file_from_s3(self, key: str, local_path: str):   
        """Download file from S3"""
        async with self.session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            config=AioConfig(signature_version='s3v4')
        ) as s3: # type: ignore[attr-defined]
            await s3.download_file(
                Bucket=self.bucket, 
                Key=key, 
                Filename=local_path
            )

    async def upload_file_s3(self, object_key: str, file: bytes, mimetype: str) -> bool:
        """Upload a file to an S3 bucket"""
        async with self.session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            config=AioConfig(signature_version='s3v4')
        ) as s3: # type: ignore[attr-defined]
            await s3.put_object(Bucket=self.bucket, Key=object_key, Body=file, ContentType=mimetype)
            return True
        
        return False

    async def head_object_from_s3(self, key: str) -> Any:
        """Returns the meta data associated with the object"""
        async with self.session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            config=AioConfig(signature_version='s3v4')
        ) as s3: # type: ignore[attr-defined]
            return await s3.head_object(Bucket=self.bucket, Key=key)
        
    
    async def get_object_s3(self, key: str):
        """Gets the object via PUT"""
        async with self.session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            config=AioConfig(signature_version='s3v4')
        ) as s3: # type: ignore[attr-defined]
            response = await s3.get_object(Bucket=self.bucket, Key=key)
            return response
        
    async def get_object_s3_stream(self, key: str):
        """Gets the object stream via PUT
        
        Returns:
            Stream bytes

            File size (content-length)
        """
        async with self.session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            config=AioConfig(signature_version='s3v4')
        ) as s3: # type: ignore[attr-defined]
            response = await s3.get_object(Bucket=self.bucket, Key=key)
            file_size = response.get('ContentLength', 0)
            body = await response['Body'].read()
            return body, file_size
    


    async def delete_file_s3(self, key: str) -> bool:
        """Delete file from S3"""
        try:
            async with self.session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            config=AioConfig(signature_version='s3v4')
        ) as s3: # type: ignore[attr-defined]
                await s3.delete_object(Bucket=self.bucket, Key=key)
                return True
        except Exception:
            return False
        
    async def copy_file_s3(self, key: str, new_key: str, mimetype: str) -> Any:
        """Delete file from S3"""
        async with self.session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            config=AioConfig(signature_version='s3v4')
        ) as s3: # type: ignore[attr-defined]
            response = s3.copy_object(
                Bucket=self.bucket,
                ContentType=mimetype,
                Key=new_key,
                CopySource={
                    'Bucket': self.bucket,
                    'Key': key
                }
            )
        
        return response
    
storage = ObjectStorage(
    bucket=settings.storage.BUCKET_NAME,
    endpoint=settings.storage.ENDPOINT,
    access_key_id=settings.storage.ACCESS_KEY_ID,
    secret_access_key=settings.storage.SECRET_ACCESS_KEY
)
"""Storage intialization with public bucket"""

storage_private = ObjectStorage(
    bucket=settings.storage.PRIVATE_BUCKET_NAME,
    endpoint=settings.storage.ENDPOINT,
    access_key_id=settings.storage.ACCESS_KEY_ID,
    secret_access_key=settings.storage.SECRET_ACCESS_KEY
)
"""Storage intialization with private bucket"""
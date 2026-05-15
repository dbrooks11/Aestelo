
from app.config import Config

class InvalidFileTypeError(Exception):
    allowed_types: str = ', '.join(Config.ALLOWED_MIME_TYPES.values())

    def __init__(self, mimetype: str | None = None):
        """Raised when file type is not allowed"""
        self.mimetype = mimetype
        self.message = f"Invalid file type: '{mimetype}'. Allowed types: {self.allowed_types}"

    def __str__(self):
        return self.message

class InvalidObjectStorageDestinationError(Exception): 
    def __init__(self, folder: str | None = None):
        """Raised when there's an invalid folder/destination for the object"""
        self.folder = folder
        self.message = f"Invalid S3/R2 folder destination: {folder}"

    def __str__(self):
        return self.message
    
class InvalidConfigurationError(Exception):
    def __init__(self, component: str, missing_field: str, message: str | None = None):
        """Raised when required configuration is missing or invalid."""
        self.component = component
        self.missing_field = missing_field
        self.message = message or f"{component} configuration error: '{missing_field}' is missing or empty"

    def __str__(self):
        return self.message
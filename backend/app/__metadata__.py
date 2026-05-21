"""Metadata for the Project."""

from importlib.metadata import PackageNotFoundError, metadata, version 

__all__ = ("__project__", "__version__") 

try:
    __version__ = version("app")
    """Version of the project."""
    __project__ = metadata("app")["Name"]
    """Name of the project."""
except PackageNotFoundError: 
    __version__ = "0.0.1"
    __project__ = "Aestelo API"
finally:  
    del version, PackageNotFoundError, metadata
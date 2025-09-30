from app import ma
from marshmallow import (fields, Schema, validates, 
                         validates_schema, ValidationError, validate)
from models.user import User
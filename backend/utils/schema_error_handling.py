from marshmallow import ValidationError

def schema_error_handling(error: ValidationError):
    return next(iter(error.messages_dict.values()))
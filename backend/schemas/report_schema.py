# schemas/report.py
from backend.app.extensions import ma
from marshmallow import ValidationError, fields, pre_load, validate, validates
from models.report import Report


class ReportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Report
        load_instance = True
        include_fk = True
    
    report_id = fields.Int(dump_only=True)
    reporter_id = fields.UUID(dump_only=True)  
    created_at = fields.DateTime(dump_only=True)
    status = fields.Str(dump_only=True)
    reviewed_by = fields.UUID(dump_only=True)
    reviewed_at = fields.DateTime(dump_only=True)
    
    # User provides these
    reported_type = fields.Str(
        required=True,
        validate=validate.OneOf(['profile', 'post', 'visit']))
    
    status = fields.Str(
        required=True,
        validate=validate.OneOf(['pending', 'reviewed', 'dismissed', 'actioned'])
    )

    reported_id = fields.Str(required=True)
    reason = fields.Str(
        required=True,
        validate=validate.OneOf([
            'spam',
            'harassment',
            'inappropriate',
            'violent',
            'sexual',
            'misinformation',
            'hate_speech',
            'copyright',
            'fake_location',
            'other'
        ]))
    
    description = fields.Str(
        required=False,
        validate=validate.Length(max=500))
    
    @validates('reported_id')
    def validate_reported_id(self, value, **kwargs):
        if not value or value.strip() == '':
            raise ValidationError("reported_id cannot be empty")
        return value
    
    @pre_load
    def strip_strings(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data

   

report_schema = ReportSchema()
# schemas/user.py
from app import ma
from models.music_track import MusicTrack
from marshmallow import validates, ValidationError, fields, validate,pre_load
from datetime import datetime


class MusicTrackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MusicTrack
        load_instance = True
        include_fk = True
        exclude = () 

    track_name = fields.Str(dump_only=True)
    artist_name = fields.Str(dump_only=True)
    album_name = fields.Str(dump_only=True)
    album_art_url = fields.Str(dump_only=True)
    preview_url = fields.Str(dump_only=True)
    music_url = fields.Str(dump_only=True)
    duration_ms = fields.Int(dump_only=True)
    times_used = fields.Int(dump_only=True)


music_track_schema = MusicTrackSchema()
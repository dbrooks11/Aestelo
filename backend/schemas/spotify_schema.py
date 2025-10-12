# schemas/user.py
from app import ma
from models.spotify_track import SpotifyTrack
from marshmallow import validates, ValidationError, fields, validate,pre_load
from datetime import datetime


class SpotifyTrackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpotifyTrack
        load_instance = True
        include_fk = True
        exclude = () 

    track_name = fields.Str(dump_only=True)
    artist_name = fields.Str(dump_only=True)
    album_name = fields.Str(dump_only=True)
    album_art_url = fields.Str(dump_only=True)
    preview_url = fields.Str(dump_only=True)
    spotify_url = fields.Str(dump_only=True)
    duration_ms = fields.Int(dump_only=True)
    times_used = fields.Int(dump_only=True)


spotify_track_schema = SpotifyTrackSchema()
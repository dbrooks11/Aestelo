# schemas/user.py
from backend.app.extensions import ma
from marshmallow import fields
from models.music_track import MusicTrack


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
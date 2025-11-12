from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..exstensions import db
from ..models.user import UserProfile, UserInfo, UserSettings, UserRole
from ..models.visit import Visit
from ..models.music_track import MusicTrack
from ..schemas.user_schema import user_profile_schema, ValidationError
from ..schemas.music_schema import music_track_schema
from ..util.music_track import search_track, set_track
from datetime import datetime, timezone


music_bp = Blueprint('music',__name__, url_prefix='/music')


@music_bp.route('/search', methods = ['GET'])
@jwt_required()
def search_song_visit():

    try:
        track_name = request.args.get('q')
        if track_name is None:
            return jsonify({'error':'Please enter a valid track name'}), 400
        
        #should get data for the track name the user searched
        track_search = search_track(track_name = track_name)
        if not track_search:
            return jsonify({'error':'No tracks exist'}), 404

        return jsonify({
            'searched_track': track_name,
            'results':track_search,
            'count': len(track_search)}), 200
    except Exception:
        return jsonify({'error':'Failed to fetch tracks'}), 500         
       
    
@music_bp.route('/visit/<int:visit_id>/add-track', methods = ['POST'])
@jwt_required()
def add_track_visit(visit_id):
    current_user = request.current_user.user.id
    visit = Visit.query.filter_by(user_profile_id = current_user, visit_id=visit_id).first()

    if not visit:
        return jsonify({'error': 'Visit does not exist'}), 404
        
    track_data = request.get_json()
    if track_data is None or 'id' not in track_data:
        return({'error':'Invalid track selected'}), 404
        
    try:
        track = MusicTrack.query.filter_by(music_track_id = track_data['id']).first()

        if track:
            track.times_used += 1
            visit.music_track_id = track.music_track_id
            db.session.commit()
            return jsonify({'message':'Track successfully added',
                            'track': music_track_schema.dump(track)}), 200
        else:
            duration_ms = track_data['duration_ms']
            minutes = duration_ms // 60000
            seconds = (duration_ms % 60000) // 1000
            duration_formatted = f"{minutes}:{seconds:02d}"
            
            new_track = MusicTrack(
                music_track_id = track_data['id'],
                track_name = track_data['name'],
                artist_name = track_data['artists'][0]['name'],
                album_name = track_data['album']['name'],
                album_art_url = track_data['album']['images'][0]['url'] if track_data['album']['images'] else None,
                preview_url =  track_data.get('preview_url'),
                music_url = track_data['external_urls']['music'],
                duration_ms = duration_ms,
                duration_formatted = duration_formatted,
                release_date = track_data['album']['release_date'],
                times_used = 1
            )

            visit.music_track_id = new_track.music_track_id
            new_track.times_used += 1

            db.session.add(new_track)
            db.session.commit()
            return jsonify({'message':'Track successfully added',
                            'track': music_track_schema.dump(new_track)}), 201
    except Exception:
        return jsonify({'error':'Failed to add track'}), 500
        

# @music_bp.route('/track/<string:music_track_id>', methods = ['GET'])
# @auth_required
# def get_track(music_track_id):
#     music_track = MusicTrack.get(music_track_id)

#     if not music_track:
#         return jsonify({'error':'Track does not exist'}), 404
    
#     data = request.get_json()

    


    
    
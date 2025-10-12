from flask import Blueprint, request, jsonify
from app import db
from models.user import UserProfile, UserInfo, UserSettings, UserRole
from models.visit import Visit
from models.spotify_track import SpotifyTrack
from exstensions import supabase
from routes.auth_required_wrapper import auth_required
from schemas.user_schema import user_profile_schema, ValidationError
from schemas.spotify_schema import spotify_track_schema
from util.spotify_track import search_track, select_track
from datetime import datetime, timezone


spotify_bp = Blueprint('spotify',__name__, url_prefix='/spotify')


@spotify_bp.route('/search-track/visit/<int:visit>', route = ['GET','POST'])
@auth_required
def search_song_visit(visit_id):
    current_user = request.current_user.user.id
    visit = Visit.active().filter_by(user_profile_id = id, visit_id = visit_id).first()

    if not visit:
        return jsonify({'error':'Visit does not exist'}), 404
    
    if request.method == 'GET':
        try:
            data = request.get_json()
            if data is None:
                return jsonify({'error':'No data provided for the track'}), 404
            
            #should get data for the track name the user searched
            track_search = search_track(token=token, track_name= data.get('track_name'))
            if not track_search:
                return jsonify({'error':'No tracks exist'}), 404

            return track_search
        except Exception:
            return jsonify({'error':'Failed to fetch tracks'}), 500            
    
    if request.method == 'POST':
            
        track_data = request.get_json()
        if track_data is None:
            return({'error':'Invalid track selected'}), 404
            
        try:
            track = SpotifyTrack.query.filter_by(spotify_track_id = track_data['id']).first()
            if track:
                track.times_used += 1
                visit.spotify_track_id = track.spotify_track_id
                db.session.commit()
                return jsonify({'message':'Track successfully added',
                                'track': spotify_track_schema.dump(track)}), 200
            else:
                duration_ms = track_data['duration_ms']
                minutes = duration_ms // 60000
                seconds = (duration_ms % 60000) // 1000
                duration_formatted = f"{minutes}:{seconds:02d}"
                
                new_track = SpotifyTrack(
                    spotify_track_id = track_data[id],
                    track_name = track_data['name'],
                    artist_name = track_data['artists'][0]['name'],
                    album_name = track_data['album']['name'],
                    album_art_url = track_data['album']['images'][0]['url'] if track_data['album']['images'] else None,
                    preview_url =  track_data.get('preview_url'),
                    spotify_url = track_data['external_urls']['spotify'],
                    duration_ms = duration_ms,
                    duration_formatted = duration_formatted,
                    release_date = track_data['album']['release_date']
                )

                visit.spotify_track_id = new_track.spotify_track_id
                new_track.times_used += 1
                db.session.add(new_track)
                db.session.commit()

                return jsonify({'message':'Track successfully added'}), 201
        except Exception:
            return jsonify({'error':'Failed to add track'}), 500
         


@spotify_bp.route('/search-track/profile-me', methods = ['POST'])
@auth_required 
def search_song_profile():
    current_user = request.current_user.user.id
    current_user_profile = UserProfile.query.get(current_user)

    if not current_user_profile or current_user_profile.is_banned:
        return jsonify({'error':'Profile does not exist'}), 404

    if current_user_profile.is_prem_account:
        

@spotify_bp.route('/track/<string:spotify_track_id>', methods = ['GET'])
@auth_required
def get_track(spotify_track_id):
    spotify_track = SpotifyTrack.get(spotify_track_id)

    if not spotify_track:
        return jsonify({'error':'Track does not exist'}), 404
    
    data = request.get_json()

    


    
    
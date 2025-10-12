from flask import current_app
from datetime import datetime, timezone, timedelta
import os
import base64
import requests 
from dotenv import load_dotenv
from models.spotify_track import SpotifyTrack
from app import db


_token_cache = {
    'access_token': None,
    'expires_at': None
}


def get_token_spotify():
    load_dotenv()

    if _token_cache['access_token'] and _token_cache['expires_at']:
        if datetime.now() < _token_cache['expires_at']:
            return _token_cache['access_token']
    
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

    encoded = base64.b64encode((f"{client_id}:{client_secret}").encode('ascii')).decode('ascii')

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded}"
    }

    payload ={
        "grant_type": "client_credentials"
    }


    #todo: Cache token for 59 mintues to reuse until it expires
    response = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)
    token = response.json()

    _token_cache['access_token'] = token['access_token']
    _token_cache['expires_at'] = datetime.now() + timedelta(seconds = 3540)

    return token['access_token']



def search_track(track_name, limit = 40):

    token = get_token_spotify()

    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'q':track_name,
        'type': 'track',
        'limit': limit
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Spotify search failed: {response.text}")
    
    data = response.json()

    tracks = []
    for track_data in data['tracks']['items']:

        duration_ms = track_data['duration_ms']
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        duration_formatted = f"{minutes}:{seconds:02d}"

        track = {
            'spotify_track_id': track_data['id'],
            'track_name': track_data['name'],
            'artist_name': track_data['artists'][0]['name'],
            'album_name': track_data['album']['name'],
            'album_art_url': track_data['album']['images'][0]['url'] if track_data['album']['images'] else None,
            'preview_url': track_data.get('preview_url'),
            'spotify_url': track_data['external_urls']['spotify'],
            'duration_ms':track_data['duration_ms'],
            'duration_formatted': duration_formatted,
            'release_date': track_data['album']['release_date']
        }

        tracks.append(track)

    return tracks


def set_track(track_data):
    track_id = track_data['id']

    track = SpotifyTrack.query.get(track_id)

    if track:
        track.times_used += 1
    else:
        duration_ms = track_data['duration_ms']
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        duration_formatted = f"{minutes}:{seconds:02d}"

        new_track = new_track = SpotifyTrack(
            spotify_track_id = track_data['id'],
            track_name = track_data['name'],
            artist_name = track_data['artists'][0]['name'],
            album_name = track_data['album']['name'],
            album_art_url = track_data['album']['images'][0]['url'] if track_data['album']['images'] else None,
            preview_url =  track_data.get('preview_url'),
            spotify_url = track_data['external_urls']['spotify'],
            duration_ms = duration_ms,
            duration_formatted = duration_formatted,
            release_date = track_data['album']['release_date'],
            times_used = 1
        )
    
    return new_track
            

    
    
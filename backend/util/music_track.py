from datetime import datetime, timedelta
import os
import base64
import requests 
from dotenv import load_dotenv
from models.music_track import MusicTrack
# from flask import current_app


_token_cache = {
    'access_token': None,
    'expires_at': None
}

def get_token_music():
    load_dotenv()

    if _token_cache['access_token'] and _token_cache['expires_at']:
        if datetime.now() < _token_cache['expires_at']:
            return _token_cache['access_token']
    
    #todo: chage from os.environ to current_app config
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
    response = requests.post("https://accounts.music.com/api/token", data=payload, headers=headers)
    token = response.json()

    _token_cache['access_token'] = token['access_token']
    _token_cache['expires_at'] = datetime.now() + timedelta(seconds = 3540)

    return token['access_token']



def search_track(track_name, limit = 5):

    token = get_token_music()

    music_search_url = "https://api.music.com/v1/search"

    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'q':track_name,
        'type': 'track',
        'limit': limit
    }

    try:
        response = requests.get(music_search_url, headers=headers, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Music search failed: {e}") 

    if response.status_code != 200:
        raise Exception(f"Music search failed: {response.text}:{response.status_code}")
    
    data = response.json()

    tracks = []
    for track_data in data.get('tracks',{}).get('items',[]):

        duration_ms = track_data.get('duration_ms')
        if duration_ms is not None:
            minutes = duration_ms // 60000
            seconds = (duration_ms % 60000) // 1000
            duration_formatted = f"{minutes}:{seconds:02d}"
        else:
            duration_formatted = None

        artist_name = track_data.get('artists', [])
        album_art_url = track_data.get('album',{}).get('images',[])

        track = {
            'music_track_id': track_data.get('id'),
            'track_name': track_data.get('name'),
            'artist_name': artist_name[0].get('name') if artist_name else None,
            'album_name': track_data.get('album', {}).get('name', None),
            'album_art_url': album_art_url[0].get('url') if album_art_url else None,
            'preview_url': track_data.get('preview_url'),
            'music_url': track_data.get('external_urls', {}).get('music', None),
            'duration_ms': duration_ms,
            'duration_formatted': duration_formatted,
            'release_date': track_data.get('album', {}).get('release_date', None)
        }

        tracks.append(track)

    return tracks



def set_track(track_data):
    track_id = track_data['id']

    track = MusicTrack.query.get(track_id)

    if track:
        track.times_used += 1
    else:
        duration_ms = track_data.get('duration_ms')
        if duration_ms is not None:
            minutes = duration_ms // 60000
            seconds = (duration_ms % 60000) // 1000
            duration_formatted = f"{minutes}:{seconds:02d}"
        else:
            duration_formatted = None
    
        artist_name = track_data.get('artists', [])
        album_art_url = track_data.get('album',{}).get('images',[])

        new_track = new_track = MusicTrack(
            music_track_id = track_data.get('id'),
            track_name = track_data.get('name'),
            artist_name = artist_name[0].get('name') if artist_name else None,
            album_name = track_data.get('album', {}).get('name', None),
            album_art_url = album_art_url[0].get('url') if album_art_url else None,
            preview_url =  track_data.get('preview_url'),
            music_url = track_data.get('external_urls', {}).get('music', None),
            duration_ms = duration_ms,
            duration_formatted = duration_formatted,
            release_date = track_data.get('album', {}).get('release_date', None),
            times_used = 1
        )

    return new_track
            
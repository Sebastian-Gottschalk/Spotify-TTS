import os
import requests
import base64
from urllib.parse import urlencode
import spotipy
import TTS
import json


base_url = "https://api.spotify.com/v1"


def read_id_secret():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    rel_path = "user_data/Spotify_API_Keys.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    keys = open(abs_file_path)
    content=keys.readlines()
    keys.close()
    client_id = content[0][:-1]
    client_secret = content[1]
    return [client_id,client_secret]


def search_song(keyword,headers):
    url = base_url + "/search"
    data = urlencode({
        "q" : keyword,
        "type" : "track"
    })
    lookup_url = f"{url}?{data}"
    req = requests.get(lookup_url, headers = headers)

    id = req.json()['tracks']['items'][0]['id']
    return id

def get_track(id,headers):
    url = base_url + f"/tracks/{id}"
    req = requests.get(url, headers = headers)
    song_name = req.json()['name']
    interpret = req.json()['album']['artists'][0]['name']
    print(song_name)
    print(interpret)
    return [song_name,interpret]

def add_to_queue(sp, id, headers):
    sp.add_to_queue(f"spotify:track:{id}")

def play_song(id, headers):
    url = base_url + f"/me/player/play"
    data = json.dumps({
        "uris" : [f"spotify:track:{id}"]
    })
    req = requests.put(url, data = data, headers = headers)

def get_recommendations(id, headers, limit):
    recoms = sp.recommendations(seed_tracks = [id], limit = limit)['tracks']
    for i in range(limit):
        current_recom = recoms[i]
        uri = current_recom['uri']
        sp.add_to_queue(uri)
    TTS.read_text(f'Added {limit} songs to the queue')

def save_in_playlist(id,headers):
    my_playlist_uri = "spotify:playlist:68FxkgffYahgQCwrtIcxE9"
    sp.playlist_add_items(my_playlist_uri, [id])
    

def use_command(command,add_info):
    if command.lower() in ['at','add']:
        id = search_song(add_info,headers)
        add_to_queue(sp,id,headers)
        names = get_track(id,headers)
        TTS.read_text(f'Added{names[0]} by {names[1]}')
    if command.lower() in ['play']:
        id = search_song(add_info,headers)
        play_song(id, headers)
        names = get_track(id,headers)
        TTS.read_text(f'Playing{names[0]} by {names[1]}')
    if command.lower() in ['recommend']:
        if add_info.split()[-1].isdigit():
            limit = int(add_info.split()[-1])
            add_info = add_info.rsplit(' ',1)[0]
            if limit > 100:
                limit = 100
            if limit < 1:
                limit = 1
        else:
            limit = 3
        if add_info == 'current':
            id = sp.current_user_playing_track()['item']['id']
        else:
            id = search_song(add_info,headers)
        recom = get_recommendations(id, headers,limit)
    if command.lower() in ['save','safe']:
        if add_info in ['song']:
            id = sp.current_user_playing_track()['item']['id']
            save_in_playlist(id,headers)
            names = get_track(id,headers)
            TTS.read_text(f'Added {names[0]} by {names[1]} to the playlist')
            


    
client_idx = read_id_secret()
client_id = client_idx[0]
client_secret = client_idx[1]
redirect_uri = "http://localhost/"
scope = "user-read-playback-state,user-modify-playback-state,playlist-modify-public,playlist-modify-private"
auth_manager = spotipy.SpotifyOAuth(
          client_id=client_id,
          client_secret=client_secret,
          redirect_uri=redirect_uri,    
          scope=scope, open_browser=False)


sp = spotipy.Spotify(auth_manager=auth_manager)

headers = {
        "Authorization" : f"Bearer {auth_manager.get_access_token()['access_token']}"
}

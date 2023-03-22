# Imports

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy

import json
import os
import requests


def text_to_spotify(playlist_text):

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # STEP 1: Get (1) playlist title & (2) song names
    if playlist_text == None:
        playlist_text = open('response.txt', 'r').read()

    playlist = playlist_text.split('\n')

    title = playlist[2].split(": ")[1]
    songs = playlist[4:]

    # STEP 2: Get playlist URIs from song & artist names

    uris = []
    # Use song name and artist to find URI (needed to add to playlist)
    for idx, song in enumerate(songs):
        res = sp.search(q=song.split(". ")[1], limit=1)
        uris.append(res['tracks']['items'][0]['uri'])

    # STEP 3: Create playlist
    #  USE: https://github.com/spotipy-dev/spotipy/blob/master/examples/create_playlist.py

    scope = "playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    user_id = os.getenv("SPOTIFY_USER_ID")
    sp.user_playlist_create(user=user_id, name=title, public=False,
                            collaborative=False, description="An auto generated playlist using ChatGPT")

    # Read current playlists to get new URI
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    results = sp.current_user_playlists(limit=10)
    for i, item in enumerate(results['items']):
        if item['name'] == title:
            playlist_uri = item['uri']

    # STEP 4: Add songs to playlist

    scope = 'playlist-modify-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    sp.playlist_add_items(playlist_uri, uris)

#  USE: https://github.com/spotipy-dev/spotipy/blob/master/examples/add_tracks_to_playlist.py

# user_id = os.getenv("SPOTIFY_USER_ID")
# oauth_token = os.getenv("SPOTIFY_OAUTH_TOKEN")

# endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

# request_body = json.dumps({
#     "name": title,
#     "description": "Test Auto Generated Playlist",
#     "public": False
# })


# response = requests.post(url=endpoint_url, data=request_body, headers={"Content-Type": "application/json",
#                                                                        "Authorization": f"Bearer {oauth_token}"})
# print(response.status_code)

# playlist_id = response.json()['id']
# endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

# songs_json = json.dumps(uris)

# response = requests.post(url=endpoint_url, data=request_body, headers={"Content-Type": "application/json",
#                                                                        "Authorization": f"Bearer {oauth_token}"})

# print(response.status_code)
# print("--------------------------------------------------------------------")
# print(results['tracks']['items'][0]['album'])
# print("--------------------------------------------------------------------")
# print(results['tracks']['items'][0]['artists'])
# print("--------------------------------------------------------------------")
# print(results['tracks']['items'][0]['name'])
# print("--------------------------------------------------------------------")
# print(results['tracks']['items'][0]['uri'])
# print(results['tracks']['items'])

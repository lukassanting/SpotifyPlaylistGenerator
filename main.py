import openai
import os
import json
import requests

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy

from query_chatGPT import generate_playlist_chatGPT
from list_to_spotify import text_to_spotify

if __name__ == "__main__":
    playlist_text = generate_playlist_chatGPT()
    text_to_spotify(playlist_text)

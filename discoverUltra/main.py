import os
from datetime import datetime
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

scope = "user-read-recently-played user-top-read playlist-modify-public playlist-modify-private playlist-read-private user-library-read user-library-modify"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope = scope,
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
    redirect_uri = os.getenv("REDIRECT_URI"),
    cache_path=".spotify_token_cache"
))

# -------------
# USER DATA
# ------------

### get top tracks (at most 50)
def get_top_tracks(limit=50):
    results = sp.current_user_top_tracks(limit=limit, time_range="short_term")
    return [track["uri"] for track in results["items"]]

# top_tracks = get_top_tracks()
# for idx, track in enumerate(top_tracks):
#    print(f"{idx + 1}. {track['name']} - {track['artists'][0]['name']}")

### get most recently played (at most, last 20 played)
def get_recently_played(limit=20):
    results = sp.current_user_recently_played(limit=limit)
    return [item["track"] for item in results["items"]]

# recent_tracks = get_recently_played(5)
# for t in recent_tracks:
#   print(t['name'], "-", t['artists'][0]['name'])

### get top artists
def get_top_artists(limit=5):
    results = sp.current_user_top_artists(limit=limit, time_range="short_term")
    return [artist["id"] for artist in results["items"]]

### create new playlist
def create_playlist():
    name = "Top Tracks " + datetime.now().strftime("%m-%d-%Y")
    playlist = sp.user_playlist_create(
        user = sp.current_user()["id"],
        name = name,
        public = False,
        description = "Custom generated weekly recommendations"
    )
    return playlist["id"]

### search for "Liked Songs"
def liked_songs(limit = 50): 
    results = sp.current_user_saved_tracks(limit = limit)
    return [item["track"]["id"] for item in results["items"]]

### adds top tracks to liked songs (no duplicates)
def add_top_to_liked():
    top_tracks = get_top_tracks(limit = 50)
    liked = liked_songs(limit = 50)

    new_tracks = [item for item in top_tracks if item not in liked]
    print(f"{len(new_tracks)} new songs detected!!!")

    if new_tracks:
        sp.current_user_saved_tracks_add(new_tracks)
        print(f"Added {len(new_tracks)} new liked songs")
    else: 
        print("No new songs added")

### add new tracks to playlist
def add_to_playlist(playlist_id, track_ids):
    sp.playlist_add_items(playlist_id, track_ids)

### MAIN

def build_playlist():
    seed_artists = get_top_artists(limit=5)
    top_tracks = get_top_tracks()
    recent_played = get_recently_played()

    add_top_to_liked()

    #playlist_id = create_playlist()
    #add_to_playlist(playlist_id, top_tracks)
    
if __name__ == "__main__":
    build_playlist()
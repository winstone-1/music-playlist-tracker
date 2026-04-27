"""
api.py - Last.fm API integration
Concepts: APIs, functions, error handling, dictionaries
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def _get(params: dict) -> dict | None:
    """Base GET request to Last.fm. All other functions use this."""
    params.update({"api_key": API_KEY, "format": "json"})
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API error: {e}")
        return None


def search_track(track_name: str, artist_name: str = "", limit: int = 5) -> list[dict]:
    """Search for tracks by name. Returns a list of raw track dicts."""
    params = {"method": "track.search", "track": track_name, "limit": limit}
    if artist_name:
        params["artist"] = artist_name
    data = _get(params)
    if not data:
        return []
    try:
        return data["results"]["trackmatches"]["track"]
    except KeyError:
        return []


def get_track_info(track_name: str, artist_name: str) -> dict | None:
    """Get detailed info for a specific track."""
    params = {"method": "track.getInfo", "track": track_name, "artist": artist_name}
    data = _get(params)
    if not data or "track" not in data:
        return None
    return data["track"]


def get_artist_info(artist_name: str) -> dict | None:
    """Get detailed info for an artist including bio and stats."""
    params = {"method": "artist.getInfo", "artist": artist_name}
    data = _get(params)
    if not data or "artist" not in data:
        return None
    return data["artist"]


def get_artist_top_tracks(artist_name: str, limit: int = 5) -> list[dict]:
    """Get top tracks for an artist."""
    params = {"method": "artist.getTopTracks", "artist": artist_name, "limit": limit}
    data = _get(params)
    if not data:
        return []
    try:
        return data["toptracks"]["track"]
    except KeyError:
        return []


def get_track_tags(track_name: str, artist_name: str) -> list[str]:
    """Get genre tags for a track."""
    params = {"method": "track.getTopTags", "track": track_name, "artist": artist_name}
    data = _get(params)
    if not data:
        return []
    try:
        tags = data["toptags"]["tag"]
        return [tag["name"].lower() for tag in tags[:5]]
    except (KeyError, TypeError):
        return []
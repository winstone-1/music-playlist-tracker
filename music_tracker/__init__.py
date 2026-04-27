"""
music_tracker package
"""

from .db import DatabaseManager, get_db
from .models import Track, Artist, Playlist
from .api import (
    search_track,
    get_track_info,
    get_artist_info,
    get_artist_top_tracks,
    get_track_tags
)
from .utils import (
    clean_name,
    parse_duration,
    format_number,
    is_valid_artist_name,
    extract_plain_text,
    slugify
)

__version__ = "1.0.0"
__all__ = [
    "DatabaseManager", "get_db",
    "Track", "Artist", "Playlist",
    "search_track", "get_track_info", "get_artist_info",
    "get_artist_top_tracks", "get_track_tags",
    "clean_name", "parse_duration", "format_number",
    "is_valid_artist_name", "extract_plain_text", "slugify"
]
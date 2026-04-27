"""
models.py - OOP: Track, Artist, and Playlist classes
Part of the music_tracker package.

Concepts demonstrated: Classes, __init__, __repr__, __str__,
methods, properties, magic methods, encapsulation
"""

from datetime import datetime


# ─── Track Class ──────────────────────────────────────────────────────────────
class Track:
    """Represents a single music track fetched from Last.fm."""

    def __init__(self, title: str, artist_name: str, duration: int = 0,
                 listeners: int = 0, playcount: int = 0, tags: list = None, url: str = ""):
        self.title = title
        self.artist_name = artist_name
        self.duration = duration        # in seconds
        self.listeners = listeners
        self.playcount = playcount
        self.tags = tags or []          # list of genre tags
        self.url = url

    def duration_formatted(self) -> str:
        """Convert duration from seconds to mm:ss string."""
        if self.duration <= 0:
            return "Unknown"
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"

    def is_popular(self) -> bool:
        """A track is popular if it has over 1 million listeners."""
        return self.listeners > 1_000_000

    def classify_length(self) -> str:
        """Classify track as short, mid, or long based on duration."""
        if self.duration <= 0:
            return "unknown"
        elif self.duration < 180:       # under 3 mins
            return "short"
        elif self.duration <= 300:      # 3–5 mins
            return "mid"
        else:                           # over 5 mins
            return "long"

    def to_tuple(self) -> tuple:
        """
        Return track data as an immutable tuple.
        Tuples are used here because track metadata fetched from an
        API should not be modified — it's a fixed snapshot.
        """
        return (self.title, self.artist_name, self.duration,
                self.listeners, self.playcount, ",".join(self.tags), self.url)

    def __repr__(self) -> str:
        return f"Track(title='{self.title}', artist='{self.artist_name}', duration='{self.duration_formatted()}')"

    def __str__(self) -> str:
        return f"🎵 {self.title} — {self.artist_name} ({self.duration_formatted()})"

    def __eq__(self, other) -> bool:
        """Two tracks are equal if they share the same title and artist."""
        if not isinstance(other, Track):
            return False
        return self.title.lower() == other.title.lower() and \
               self.artist_name.lower() == other.artist_name.lower()

    def __hash__(self):
        """Allows Track objects to be stored in a set."""
        return hash((self.title.lower(), self.artist_name.lower()))


# ─── Artist Class ─────────────────────────────────────────────────────────────
class Artist:
    """Represents a music artist fetched from Last.fm."""

    def __init__(self, name: str, listeners: int = 0,
                 playcount: int = 0, bio: str = "", url: str = ""):
        self.name = name
        self.listeners = listeners
        self.playcount = playcount
        self.bio = bio
        self.url = url

    def short_bio(self, max_chars: int = 150) -> str:
        """Return a truncated version of the artist bio."""
        if not self.bio:
            return "No bio available."
        return self.bio[:max_chars] + "..." if len(self.bio) > max_chars else self.bio

    def is_mainstream(self) -> bool:
        """Artist is mainstream if listeners exceed 5 million."""
        return self.listeners > 5_000_000

    def to_tuple(self) -> tuple:
        """Return artist data as an immutable tuple."""
        return (self.name, self.listeners, self.playcount, self.bio, self.url)

    def __repr__(self) -> str:
        return f"Artist(name='{self.name}', listeners={self.listeners:,})"

    def __str__(self) -> str:
        return f"🎤 {self.name} — {self.listeners:,} listeners"


# ─── Playlist Class ───────────────────────────────────────────────────────────
class Playlist:
    """
    Represents a user-created playlist containing Track objects.
    Demonstrates: encapsulation, list operations, set usage,
    iteration, and computed properties.
    """

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self._tracks: list[Track] = []      # private — access via methods
        self.created_at = datetime.now()

    def add_track(self, track: Track) -> bool:
        """
        Add a track to the playlist.
        Returns False if the track already exists (uses __eq__).
        """
        if track in self._tracks:
            print(f"⚠️  '{track.title}' is already in '{self.name}'")
            return False
        self._tracks.append(track)
        print(f"✅ Added: {track}")
        return True

    def remove_track(self, title: str) -> bool:
        """Remove a track by title. Returns True if found and removed."""
        for track in self._tracks:
            if track.title.lower() == title.lower():
                self._tracks.remove(track)
                print(f"🗑️  Removed: '{title}'")
                return True
        print(f"❌ Track '{title}' not found.")
        return False

    def total_duration(self) -> str:
        """Calculate total playlist duration and return as h:mm:ss."""
        total_seconds = sum(t.duration for t in self._tracks)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    def unique_artists(self) -> set:
        """
        Return a set of unique artist names in this playlist.
        Sets automatically remove duplicates — perfect for this.
        """
        return {track.artist_name for track in self._tracks}

    def unique_tags(self) -> set:
        """Return all unique genre tags across all tracks."""
        all_tags = set()
        for track in self._tracks:
            all_tags.update(track.tags)
        return all_tags

    def get_tracks(self) -> list:
        """Return a copy of the tracks list."""
        return list(self._tracks)

    def track_count(self) -> int:
        return len(self._tracks)

    def summary(self) -> str:
        """Print a formatted playlist summary."""
        lines = [
            f"\n📀 Playlist: {self.name}",
            f"   {self.description}",
            f"   Tracks     : {self.track_count()}",
            f"   Duration   : {self.total_duration()}",
            f"   Artists    : {len(self.unique_artists())}",
            f"   Tags       : {', '.join(self.unique_tags()) or 'None'}",
            f"   Created    : {self.created_at.strftime('%Y-%m-%d %H:%M')}",
        ]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Playlist(name='{self.name}', tracks={self.track_count()})"

    def __str__(self) -> str:
        return self.summary()

    def __len__(self) -> int:
        return self.track_count()

    def __iter__(self):
        """Makes the playlist directly iterable — for track in playlist."""
        return iter(self._tracks)
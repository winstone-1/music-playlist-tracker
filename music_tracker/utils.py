"""
utils.py - Regex and helper utilities
Concepts: Regex, string manipulation, type conversion
"""

import re


def clean_name(name: str) -> str:
    """
    Remove special characters from artist/track names.
    Keeps letters, numbers, spaces, hyphens, apostrophes.
    """
    if not name:
        return ""
    cleaned = re.sub(r"[^\w\s\-\']", "", name)
    return cleaned.strip()


def parse_duration(duration_str: str) -> int:
    """
    Convert a duration string to total seconds.
    Handles formats: '3:45', '1:03:22', or raw seconds as string '214'.
    Returns 0 if parsing fails.
    """
    if not duration_str:
        return 0

    # Already a plain number (seconds from API)
    if re.fullmatch(r"\d+", duration_str.strip()):
        return int(duration_str.strip())

    # mm:ss format
    match = re.fullmatch(r"(\d+):(\d{2})", duration_str.strip())
    if match:
        return int(match.group(1)) * 60 + int(match.group(2))

    # hh:mm:ss format
    match = re.fullmatch(r"(\d+):(\d{2}):(\d{2})", duration_str.strip())
    if match:
        return int(match.group(1)) * 3600 + int(match.group(2)) * 60 + int(match.group(3))

    return 0


def format_number(n: int) -> str:
    """Format large numbers with commas. e.g. 1000000 → '1,000,000'"""
    return f"{n:,}"


def is_valid_artist_name(name: str) -> bool:
    """
    Validate an artist name using regex.
    Must be 1–100 characters, no purely numeric names.
    """
    if not name or not isinstance(name, str):
        return False
    name = name.strip()
    if re.fullmatch(r"\d+", name):
        return False
    return bool(re.match(r"^[\w\s\-\'\.\&]{1,100}$", name))


def extract_plain_text(bio: str) -> str:
    """
    Strip HTML tags from Last.fm bio text.
    Last.fm bios sometimes contain <a> tags.
    """
    if not bio:
        return ""
    clean = re.sub(r"<[^>]+>", "", bio)        # remove HTML tags
    clean = re.sub(r"\s+", " ", clean)          # collapse whitespace
    return clean.strip()


def slugify(name: str) -> str:
    """
    Convert a name to a URL-friendly slug.
    e.g. 'Late Night Vibes!' → 'late-night-vibes'
    """
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")
"""
db.py - Database connection manager and schema setup
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "music_tracker.db")

class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        print(f"✅ Connected to database: {self.db_path}")
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            print("🔒 Database connection closed.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create_tables(self):
        if not self.connection:
            raise RuntimeError("Not connected. Call connect() first.")
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artists (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL UNIQUE,
                listeners   INTEGER DEFAULT 0,
                playcount   INTEGER DEFAULT 0,
                bio         TEXT,
                url         TEXT,
                created_at  TEXT    DEFAULT (datetime('now'))
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                artist_name TEXT    NOT NULL,
                duration    INTEGER DEFAULT 0,
                listeners   INTEGER DEFAULT 0,
                playcount   INTEGER DEFAULT 0,
                tags        TEXT,
                url         TEXT,
                created_at  TEXT    DEFAULT (datetime('now')),
                UNIQUE(title, artist_name)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL UNIQUE,
                description TEXT,
                created_at  TEXT    DEFAULT (datetime('now'))
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlist_tracks (
                playlist_id INTEGER NOT NULL,
                track_id    INTEGER NOT NULL,
                position    INTEGER NOT NULL,
                added_at    TEXT    DEFAULT (datetime('now')),
                PRIMARY KEY (playlist_id, track_id),
                FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
                FOREIGN KEY (track_id)    REFERENCES tracks(id)    ON DELETE CASCADE
            )
        """)
        self.connection.commit()
        print("✅ All tables created successfully.")

def get_db(db_path: str = DB_PATH) -> DatabaseManager:
    return DatabaseManager(db_path)
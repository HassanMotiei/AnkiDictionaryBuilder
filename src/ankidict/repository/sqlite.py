import sqlite3

from ankidict.core.models import DictionaryEntry
from ankidict.repository.base import BaseRepository


class SQLiteRepository(BaseRepository):

    def __init__(self, db_path: str):

        self.conn = sqlite3.connect(db_path)

        self.conn.row_factory = sqlite3.Row

        self.create_tables()

    def create_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            word TEXT UNIQUE NOT NULL,

            ipa TEXT,

            part_of_speech TEXT,

            html TEXT,

            audio TEXT

        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS meanings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            entry_id INTEGER,

            meaning TEXT,

            sort_order INTEGER,

            FOREIGN KEY(entry_id)
                REFERENCES entries(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS examples (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            entry_id INTEGER,

            english TEXT,

            persian TEXT,

            FOREIGN KEY(entry_id)
                REFERENCES entries(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS phrases (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            entry_id INTEGER,

            english TEXT,

            persian TEXT,

            FOREIGN KEY(entry_id)
                REFERENCES entries(id)
        )
        """)
        
    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
        

    def save(self, entry: DictionaryEntry):
        
        assert isinstance(entry.word, str)
        assert isinstance(entry.ipa, str)
        assert isinstance(entry.part_of_speech, str)

        cursor = self.conn.cursor()

        # 1. find existing entry
        cursor.execute(
            "SELECT id FROM entries WHERE word = ?",
            (entry.word,)
        )

        row = cursor.fetchone()

        if row:
            entry_id = row["id"]

            cursor.execute(
                "DELETE FROM meanings WHERE entry_id = ?",
                (entry_id,)
            )

            cursor.execute(
                "DELETE FROM examples WHERE entry_id = ?",
                (entry_id,)
            )

            cursor.execute(
                "DELETE FROM phrases WHERE entry_id = ?",
                (entry_id,)
            )

            cursor.execute(
                """
                UPDATE entries
                SET ipa=?, part_of_speech=?, html=?, audio=?
                WHERE id=?
                """,
                (
                    entry.ipa,
                    entry.part_of_speech,
                    entry.html,
                    entry.audio,
                    entry_id,
                ),
            )

        else:

            cursor.execute(
                """
                INSERT INTO entries
                (word, ipa, part_of_speech, html, audio)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    entry.word,
                    entry.ipa,
                    entry.part_of_speech,
                    entry.html,
                    entry.audio,
                ),
            )

            entry_id = cursor.lastrowid

        # 2. meanings (ONLY HERE list is allowed)

        for i, meaning in enumerate(entry.meanings):

            cursor.execute(
                """
                INSERT INTO meanings
                (entry_id, meaning, sort_order)
                VALUES (?, ?, ?)
                """,
                (entry_id, meaning, i)
            )

            cursor.execute(
                """
                INSERT INTO meanings
                (entry_id, meaning, sort_order)
                VALUES (?, ?, ?)
                """,
                (entry_id, meaning, i)
            )

        # 3. examples
        for ex in entry.examples:

            cursor.execute(
                """
                INSERT INTO examples
                (entry_id, english, persian)
                VALUES (?, ?, ?)
                """,
                (entry_id, ex.english, ex.persian)
            )

        # 4. commit once
        def commit(self):
            self.conn.commit()

        def close(self):
            self.conn.close()
    
    
    def get(self, word: str):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM entries
            WHERE word = ?
            """,
            (word,) 
        )

        return cursor.fetchone()

    def exists(self, word: str) -> bool:

        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT 1 FROM entries WHERE word = ?",
            (word,)
        )

        return cursor.fetchone() is not None
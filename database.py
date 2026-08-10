import sqlite3
from datetime import datetime

DB_NAME = "internlens.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS internship_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            internship_name TEXT,
            source_platform TEXT,
            source_url TEXT UNIQUE,
            title TEXT,
            snippet TEXT,
            author_or_channel TEXT,
            date_posted TEXT,
            date_pulled TEXT,
            raw_score INTEGER
        )
        """
    )

    conn.commit()
    conn.close()


def save_to_db(results, internship_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    inserted = 0

    for item in results:
        try:
            cursor.execute(
                """
                INSERT INTO internship_reviews (
                    internship_name,
                    source_platform,
                    source_url,
                    title,
                    snippet,
                    author_or_channel,
                    date_posted,
                    date_pulled,
                    raw_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    internship_name,
                    item.get("platform"),
                    item.get("url"),
                    item.get("title"),
                    item.get("body", "")[:300],
                    item.get("author"),
                    item.get("date_posted"),
                    datetime.utcnow().isoformat(),
                    item.get("raw_score")
                )
            )
            inserted += 1

        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

    return inserted
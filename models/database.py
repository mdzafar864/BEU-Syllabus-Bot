"""
SQLite storage for the bot (standard-library sqlite3 only).

Tables
------
bot_stats          single row: total_users, active_today, total_downloads
popular_downloads  one row per (semester, session, branch) with a download counter
button_clicks      one row per command/button with a click counter
users              every user ID ever seen (used for unique/active counts + broadcast)
feedback           feedback messages stored together with the sender's user ID
"""
import logging
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS bot_stats (
    id              INTEGER PRIMARY KEY CHECK (id = 1),
    total_users     INTEGER NOT NULL DEFAULT 0,
    active_today    INTEGER NOT NULL DEFAULT 0,
    total_downloads INTEGER NOT NULL DEFAULT 0,
    last_reset      TEXT
);

CREATE TABLE IF NOT EXISTS users (
    user_id          INTEGER PRIMARY KEY,
    first_seen       TEXT NOT NULL,
    last_active_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS popular_downloads (
    semester      TEXT NOT NULL,
    session       TEXT NOT NULL,
    branch        TEXT NOT NULL,
    downloads     INTEGER NOT NULL DEFAULT 0,
    last_download TEXT,
    PRIMARY KEY (semester, session, branch)
);

CREATE TABLE IF NOT EXISTS button_clicks (
    button       TEXT PRIMARY KEY,
    clicks       INTEGER NOT NULL DEFAULT 0,
    last_clicked TEXT
);

CREATE TABLE IF NOT EXISTS feedback (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    username    TEXT,
    first_name  TEXT,
    last_name   TEXT,
    message     TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    replied     INTEGER NOT NULL DEFAULT 0,
    reply_text  TEXT,
    replied_at  TEXT
);
CREATE INDEX IF NOT EXISTS idx_feedback_user ON feedback(user_id);
"""


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Database:
    """Thread-safe wrapper around one SQLite connection."""

    def __init__(self, path):
        self.path = str(path)
        self._lock = threading.RLock()
        # The bot handles messages on several threads -> share one connection
        # and serialise access with a lock.
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.init_db()

    # ---------- setup ----------
    def init_db(self):
        with self._tx() as cur:
            cur.executescript(SCHEMA)
            cur.execute("INSERT OR IGNORE INTO bot_stats (id) VALUES (1)")
        logger.info(f"SQLite database ready: {self.path}")

    @contextmanager
    def _tx(self):
        """Run a block inside a locked transaction (commit / rollback)."""
        with self._lock:
            cur = self.conn.cursor()
            try:
                yield cur
                self.conn.commit()
            except Exception:
                self.conn.rollback()
                raise
            finally:
                cur.close()

    def query(self, sql: str, params: tuple = ()) -> List[sqlite3.Row]:
        with self._lock:
            cur = self.conn.execute(sql, params)
            rows = cur.fetchall()
            cur.close()
            return rows

    def backup_to(self, dest_path: str):
        """Write a consistent snapshot of the DB to dest_path (for admin export)."""
        with self._lock:
            dest = sqlite3.connect(dest_path)
            try:
                self.conn.backup(dest)
            finally:
                dest.close()

    # ---------- feedback ----------
    def add_feedback(self, user_id: int, username: Optional[str], first_name: Optional[str],
                     last_name: Optional[str], message: str) -> int:
        with self._tx() as cur:
            cur.execute(
                "INSERT INTO feedback (user_id, username, first_name, last_name, message, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, username, first_name, last_name, message, now_str()),
            )
            return cur.lastrowid

    def get_recent_feedback(self, limit: int = 10) -> List[sqlite3.Row]:
        return self.query(
            "SELECT * FROM feedback ORDER BY id DESC LIMIT ?", (limit,)
        )

    def count_unreplied_feedback(self) -> int:
        return self.query("SELECT COUNT(*) AS c FROM feedback WHERE replied = 0")[0]["c"]

    def mark_feedback_replied(self, user_id: int, reply_text: str) -> int:
        """Mark all still-unanswered feedback from this user as replied."""
        with self._tx() as cur:
            cur.execute(
                "UPDATE feedback SET replied = 1, reply_text = ?, replied_at = ? "
                "WHERE user_id = ? AND replied = 0",
                (reply_text, now_str(), user_id),
            )
            return cur.rowcount

    def user_exists(self, user_id: int) -> bool:
        return bool(self.query("SELECT 1 FROM users WHERE user_id = ?", (user_id,)))

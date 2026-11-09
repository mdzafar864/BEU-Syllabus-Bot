import json
import logging
import os
from datetime import date
from typing import List, Tuple

from models.database import Database, now_str

logger = logging.getLogger(__name__)


class Analytics:
    """SQLite-backed usage statistics.

    Public API is kept close to the old JSON-based class so handlers only need
    small changes. All data lives in models/database.py's tables.
    """

    def __init__(self, db_path="bot_data.db", legacy_json: str = None):
        self.db = Database(db_path)
        if legacy_json:
            self._import_legacy_json(legacy_json)

    # ---------- internal ----------
    @staticmethod
    def _today() -> str:
        return date.today().isoformat()

    def _roll_day(self, cur):
        """Reset the 'active today' counter when the calendar day has changed."""
        today = self._today()
        cur.execute(
            "UPDATE bot_stats SET active_today = 0, last_reset = ? "
            "WHERE id = 1 AND (last_reset IS NULL OR last_reset != ?)",
            (today, today),
        )

    def _touch_user(self, cur, user_id: int):
        """Register the user / mark them active today, keeping bot_stats in sync."""
        today = self._today()
        self._roll_day(cur)
        cur.execute(
            "INSERT OR IGNORE INTO users (user_id, first_seen, last_active_date) VALUES (?, ?, ?)",
            (user_id, now_str(), today),
        )
        if cur.rowcount == 1:  # brand-new user
            cur.execute(
                "UPDATE bot_stats SET total_users = total_users + 1, "
                "active_today = active_today + 1 WHERE id = 1"
            )
        else:
            cur.execute(
                "UPDATE users SET last_active_date = ? WHERE user_id = ? AND last_active_date != ?",
                (today, user_id, today),
            )
            if cur.rowcount == 1:  # first activity of the day
                cur.execute("UPDATE bot_stats SET active_today = active_today + 1 WHERE id = 1")

    # ---------- tracking ----------
    def track_user(self, user_id: int, command: str = "start"):
        """Record activity by a user and a click on a command/button."""
        try:
            with self.db._tx() as cur:
                self._touch_user(cur, user_id)
                cur.execute(
                    "INSERT INTO button_clicks (button, clicks, last_clicked) VALUES (?, 1, ?) "
                    "ON CONFLICT(button) DO UPDATE SET clicks = clicks + 1, last_clicked = excluded.last_clicked",
                    (command, now_str()),
                )
        except Exception as e:
            logger.error(f"track_user failed: {e}")

    def track_download(self, user_id: int, semester: str, branch: str, session: str):
        """Record a syllabus download for (semester, session, branch)."""
        try:
            with self.db._tx() as cur:
                self._touch_user(cur, user_id)
                cur.execute(
                    "INSERT INTO popular_downloads (semester, session, branch, downloads, last_download) "
                    "VALUES (?, ?, ?, 1, ?) "
                    "ON CONFLICT(semester, session, branch) DO UPDATE SET "
                    "downloads = downloads + 1, last_download = excluded.last_download",
                    (semester, session, branch, now_str()),
                )
                cur.execute("UPDATE bot_stats SET total_downloads = total_downloads + 1 WHERE id = 1")
        except Exception as e:
            logger.error(f"track_download failed: {e}")

    def reset_daily(self):
        """Reset the 'active today' counter (also happens automatically on a new day)."""
        try:
            with self.db._tx() as cur:
                cur.execute(
                    "UPDATE bot_stats SET active_today = 0, last_reset = ? WHERE id = 1",
                    (self._today(),),
                )
            logger.info("Daily analytics reset completed")
        except Exception as e:
            logger.error(f"reset_daily failed: {e}")

    # ---------- reading ----------
    def _stat(self, column: str) -> int:
        # make sure a stale 'active_today' from yesterday is never shown
        with self.db._tx() as cur:
            self._roll_day(cur)
        return self.db.query(f"SELECT {column} AS v FROM bot_stats WHERE id = 1")[0]["v"]

    def get_total_users(self) -> int:
        return self._stat("total_users")

    def get_active_today(self) -> int:
        return self._stat("active_today")

    def get_total_downloads(self) -> int:
        return self._stat("total_downloads")

    def get_file_downloads(self, semester: str, session: str, branch: str) -> int:
        rows = self.db.query(
            "SELECT downloads FROM popular_downloads WHERE semester = ? AND session = ? AND branch = ?",
            (semester, session, branch),
        )
        return rows[0]["downloads"] if rows else 0

    def get_top_downloads(self, limit: int = 10) -> List[Tuple[str, str, str, int]]:
        """[(semester, session, branch, downloads), ...] most popular first."""
        rows = self.db.query(
            "SELECT semester, session, branch, downloads FROM popular_downloads "
            "ORDER BY downloads DESC, last_download DESC LIMIT ?",
            (limit,),
        )
        return [(r["semester"], r["session"], r["branch"], r["downloads"]) for r in rows]

    def get_button_stats(self, limit: int = 10) -> List[Tuple[str, int]]:
        rows = self.db.query(
            "SELECT button, clicks FROM button_clicks ORDER BY clicks DESC LIMIT ?", (limit,)
        )
        return [(r["button"], r["clicks"]) for r in rows]

    def get_all_user_ids(self) -> List[int]:
        return [r["user_id"] for r in self.db.query("SELECT user_id FROM users")]

    def export_db(self, dest_path: str):
        self.db.backup_to(dest_path)

    # ---------- one-time migration ----------
    def _import_legacy_json(self, path: str):
        """Carry over users and command counts from the old analytics.json (only once)."""
        try:
            if not os.path.exists(path) or self.db.query("SELECT 1 FROM users LIMIT 1"):
                return
            with open(path, "r") as f:
                data = json.load(f)
            today = self._today()
            with self.db._tx() as cur:
                for uid in data.get("total_users", []):
                    cur.execute(
                        "INSERT OR IGNORE INTO users (user_id, first_seen, last_active_date) VALUES (?, ?, ?)",
                        (int(uid), now_str(), "1970-01-01"),
                    )
                for button, clicks in data.get("command_stats", {}).items():
                    cur.execute(
                        "INSERT INTO button_clicks (button, clicks, last_clicked) VALUES (?, ?, ?) "
                        "ON CONFLICT(button) DO UPDATE SET clicks = clicks + excluded.clicks",
                        (button, int(clicks), now_str()),
                    )
                cur.execute(
                    "UPDATE bot_stats SET total_users = (SELECT COUNT(*) FROM users), last_reset = ? WHERE id = 1",
                    (today,),
                )
            logger.info(f"Imported legacy analytics from {path}")
        except Exception as e:
            logger.error(f"Legacy analytics import failed: {e}")

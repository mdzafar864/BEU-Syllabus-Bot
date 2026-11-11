import json
import logging
import os
from datetime import date
from typing import List, Tuple

from models.database import Database, now_str

logger = logging.getLogger(__name__)


class Analytics:
    """MongoDB-backed usage statistics.

    Public API is unchanged from the previous version so handlers need no changes.
    All data lives in the collections defined in models/database.py.
    """

    def __init__(self, mongo_uri: str, db_name: str = "beu_syllabus_bot", legacy_json: str = None):
        self.db = Database(mongo_uri, db_name)
        if legacy_json:
            self._import_legacy_json(legacy_json)

    # ---------- internal ----------
    @staticmethod
    def _today() -> str:
        return date.today().isoformat()

    def _touch_user(self, user_id: int):
        """Register the user (if new) and mark them active today. Atomic upsert."""
        self.db.users.update_one(
            {"_id": user_id},
            {
                "$setOnInsert": {"first_seen": now_str()},
                "$set": {"last_active_date": self._today()},
            },
            upsert=True,
        )

    # ---------- tracking ----------
    def track_user(self, user_id: int, command: str = "start"):
        """Record activity by a user and a click on a command/button."""
        try:
            self._touch_user(user_id)
            self.db.button_clicks.update_one(
                {"_id": command},
                {"$inc": {"clicks": 1}, "$set": {"last_clicked": now_str()}},
                upsert=True,
            )
        except Exception as e:
            logger.error(f"track_user failed: {e}")

    def track_download(self, user_id: int, semester: str, branch: str, session: str):
        """Record a syllabus download for (semester, session, branch)."""
        try:
            self._touch_user(user_id)
            self.db.popular_downloads.update_one(
                {"semester": semester, "session": session, "branch": branch},
                {"$inc": {"downloads": 1}, "$set": {"last_download": now_str()}},
                upsert=True,
            )
            self.db.bot_stats.update_one(
                {"_id": "global"}, {"$inc": {"total_downloads": 1}}, upsert=True
            )
        except Exception as e:
            logger.error(f"track_download failed: {e}")

    def reset_daily(self):
        """'Active today' is derived from each user's last_active_date, so the
        counter rolls over by itself at midnight. Kept for API compatibility."""
        logger.info("Daily analytics rollover (active-today is date-based, nothing to reset)")

    # ---------- reading ----------
    def get_total_users(self) -> int:
        return self.db.users.count_documents({})

    def get_active_today(self) -> int:
        return self.db.users.count_documents({"last_active_date": self._today()})

    def get_total_downloads(self) -> int:
        doc = self.db.bot_stats.find_one({"_id": "global"})
        return doc.get("total_downloads", 0) if doc else 0

    def get_file_downloads(self, semester: str, session: str, branch: str) -> int:
        doc = self.db.popular_downloads.find_one(
            {"semester": semester, "session": session, "branch": branch}
        )
        return doc["downloads"] if doc else 0

    def get_top_downloads(self, limit: int = 10) -> List[Tuple[str, str, str, int]]:
        """[(semester, session, branch, downloads), ...] most popular first."""
        cursor = self.db.popular_downloads.find().sort(
            [("downloads", -1), ("last_download", -1)]
        ).limit(limit)
        return [(r["semester"], r["session"], r["branch"], r["downloads"]) for r in cursor]

    def get_button_stats(self, limit: int = 10) -> List[Tuple[str, int]]:
        cursor = self.db.button_clicks.find().sort("clicks", -1).limit(limit)
        return [(r["_id"], r["clicks"]) for r in cursor]

    def get_all_user_ids(self) -> List[int]:
        return [r["_id"] for r in self.db.users.find({}, {"_id": 1})]

    def export_db(self, dest_path: str):
        self.db.export_json(dest_path)

    # ---------- one-time migration ----------
    def _import_legacy_json(self, path: str):
        """Carry over users and command counts from the old analytics.json (only once)."""
        try:
            if not os.path.exists(path) or self.db.users.count_documents({}, limit=1):
                return
            with open(path, "r") as f:
                data = json.load(f)
            for uid in data.get("total_users", []):
                self.db.users.update_one(
                    {"_id": int(uid)},
                    {"$setOnInsert": {"first_seen": now_str(), "last_active_date": "1970-01-01"}},
                    upsert=True,
                )
            for button, clicks in data.get("command_stats", {}).items():
                self.db.button_clicks.update_one(
                    {"_id": button},
                    {"$inc": {"clicks": int(clicks)}, "$set": {"last_clicked": now_str()}},
                    upsert=True,
                )
            logger.info(f"Imported legacy analytics from {path}")
        except Exception as e:
            logger.error(f"Legacy analytics import failed: {e}")

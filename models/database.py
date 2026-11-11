"""
MongoDB Atlas storage for the bot (PyMongo).

Collections
-----------
users              one document per user ID ever seen (_id = Telegram user ID)
popular_downloads  one document per (semester, session, branch) with a download counter
button_clicks      one document per command/button (_id = button name) with a click counter
feedback           feedback messages stored together with the sender's user ID
bot_stats          single document (_id = "global") holding total_downloads
counters           auto-increment sequences (used for feedback numbers)

PyMongo's MongoClient is thread-safe, so one shared client is used by all handlers.
"""
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from pymongo import ASCENDING, DESCENDING, MongoClient, ReturnDocument
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Database:
    """Thin wrapper around a MongoDB Atlas database."""

    def __init__(self, uri: str, db_name: str = "beu_syllabus_bot"):
        if not uri:
            raise ValueError("MONGO_URI environment variable is required")
        self.client = MongoClient(uri, serverSelectionTimeoutMS=10000)
        self.db = self.client[db_name]

        self.users = self.db["users"]
        self.popular_downloads = self.db["popular_downloads"]
        self.button_clicks = self.db["button_clicks"]
        self.feedback = self.db["feedback"]
        self.bot_stats = self.db["bot_stats"]
        self.counters = self.db["counters"]

        self.init_db()

    # ---------- setup ----------
    def init_db(self):
        # Fail fast (with a clear error) if Atlas is unreachable / credentials are wrong
        self.client.admin.command("ping")

        self.users.create_index([("last_active_date", ASCENDING)])
        self.popular_downloads.create_index(
            [("semester", ASCENDING), ("session", ASCENDING), ("branch", ASCENDING)],
            unique=True,
        )
        self.popular_downloads.create_index([("downloads", DESCENDING)])
        self.button_clicks.create_index([("clicks", DESCENDING)])
        self.feedback.create_index([("id", DESCENDING)], unique=True)
        self.feedback.create_index([("user_id", ASCENDING), ("replied", ASCENDING)])

        self.bot_stats.update_one(
            {"_id": "global"}, {"$setOnInsert": {"total_downloads": 0}}, upsert=True
        )
        logger.info(f"MongoDB connected: database '{self.db.name}'")

    def _next_id(self, name: str) -> int:
        doc = self.counters.find_one_and_update(
            {"_id": name},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return doc["seq"]

    # ---------- feedback ----------
    def add_feedback(self, user_id: int, username: Optional[str], first_name: Optional[str],
                     last_name: Optional[str], message: str) -> int:
        feedback_id = self._next_id("feedback")
        self.feedback.insert_one({
            "id": feedback_id,
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "message": message,
            "created_at": now_str(),
            "replied": False,
            "reply_text": None,
            "replied_at": None,
        })
        return feedback_id

    def get_recent_feedback(self, limit: int = 10) -> List[Dict[str, Any]]:
        return list(self.feedback.find({}, {"_id": 0}).sort("id", DESCENDING).limit(limit))

    def count_unreplied_feedback(self) -> int:
        return self.feedback.count_documents({"replied": False})

    def mark_feedback_replied(self, user_id: int, reply_text: str) -> int:
        """Mark all still-unanswered feedback from this user as replied."""
        result = self.feedback.update_many(
            {"user_id": user_id, "replied": False},
            {"$set": {"replied": True, "reply_text": reply_text, "replied_at": now_str()}},
        )
        return result.modified_count

    def user_exists(self, user_id: int) -> bool:
        return self.users.count_documents({"_id": user_id}, limit=1) > 0

    # ---------- export ----------
    def export_json(self, dest_path: str):
        """Dump every collection to a JSON file (for the admin export button)."""
        from bson import json_util

        payload = {
            name: list(self.db[name].find({}))
            for name in ("users", "popular_downloads", "button_clicks",
                         "feedback", "bot_stats")
        }
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(json_util.dumps(payload, indent=2, ensure_ascii=False))

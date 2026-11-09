import os
import json
import threading
import logging
from typing import Set, Dict
from datetime import date

logger = logging.getLogger(__name__)

class Analytics:
    def __init__(self, filename: str = "analytics.json"):
        self.filename = filename
        self.total_users: Set[int] = set()
        self.daily_active: Set[int] = set()
        self.command_stats: Dict[str, int] = {}
        self.daily_downloads: Dict[str, int] = {}
        self.lock = threading.Lock()
        self.load()
    
    def load(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    with self.lock:
                        self.total_users = set(data.get('total_users', []))
                        self.daily_active = set(data.get('daily_active', []))
                        self.command_stats = data.get('command_stats', {})
                        self.daily_downloads = data.get('daily_downloads', {})
                    logger.info("Analytics loaded successfully")
        except Exception as e:
            logger.error(f"Error loading analytics: {e}")
            self.save()
    
    def save(self):
        try:
            with self.lock:
                with open(self.filename, 'w') as f:
                    json.dump({
                        'total_users': list(self.total_users),
                        'daily_active': list(self.daily_active),
                        'command_stats': self.command_stats,
                        'daily_downloads': self.daily_downloads,
                        'last_reset': str(date.today())
                    }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving analytics: {e}")
    
    def track_user(self, user_id: int, command: str = "start"):
        with self.lock:
            self.total_users.add(user_id)
            self.daily_active.add(user_id)
            self.command_stats[command] = self.command_stats.get(command, 0) + 1
        self.save()
    
    def track_download(self, user_id: int, semester: str, branch: str, session: str = None):
        # Key format: "<semester>_<session>_<branch>" (session optional for legacy keys)
        key = f"{semester}_{session}_{branch}" if session else f"{semester}_{branch}"
        with self.lock:
            self.total_users.add(user_id)
            self.daily_active.add(user_id)
            self.daily_downloads[key] = self.daily_downloads.get(key, 0) + 1
        self.save()
    
    def reset_daily(self):
        with self.lock:
            self.daily_active.clear()
            self.daily_downloads.clear()
        self.save()
        logger.info("Daily analytics reset completed")
    
    def get_total_downloads(self) -> int:
        return sum(self.daily_downloads.values())
    
    def get_top_downloads(self, limit: int = 10) -> list:
        return sorted(self.daily_downloads.items(), key=lambda x: x[1], reverse=True)[:limit]

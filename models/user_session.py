import threading
from typing import Dict, Optional, Any

class UserSession:
    def __init__(self):
        self.data: Dict[int, Dict] = {}
        self.lock = threading.Lock()
    
    def get(self, user_id: int) -> Optional[Dict]:
        with self.lock:
            return self.data.get(user_id)
    
    def set(self, user_id: int, key: str, value: Any):
        with self.lock:
            if user_id not in self.data:
                self.data[user_id] = {}
            self.data[user_id][key] = value
    
    def clear(self, user_id: int):
        with self.lock:
            if user_id in self.data:
                del self.data[user_id]
    
    def get_branch(self, user_id: int) -> Optional[str]:
        session = self.get(user_id)
        return session.get('selected_branch') if session else None
    
    def get_step(self, user_id: int) -> Optional[str]:
        session = self.get(user_id)
        return session.get('step') if session else None
import json
import os


class MemoryStore:
    """Persistent memory store for user profiles and assistant context."""

    def __init__(self, path="backend/memory.json"):
        self.path = path
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            return {}

    def _save(self):
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump(self.data, handle, indent=2)

    def set(self, key: str, value):
        self.data[key] = value
        self._save()

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def save_profile(self, profile):
        user_id = profile.get("id") or profile.get("email") or "anonymous"
        self.data[f"profile:{user_id}"] = profile
        self._save()
        return profile

    def get_profile(self, user_id):
        return self.data.get(f"profile:{user_id}")

    def save_session(self, user_id: str, session: dict):
        self.data[f"session:{user_id}"] = session
        self._save()
        return session

    def get_session(self, user_id: str):
        return self.data.get(f"session:{user_id}", {})

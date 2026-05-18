from datetime import datetime, timezone

class Task:
    def __init__(self, task_id, title, description=""):
        self.id = task_id
        self.title = title
        self.description = description
        self.done = False
        # Python 3.12+ üçün timezone-aware UTC formatı
        self.created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "created_at": self.created_at
        }

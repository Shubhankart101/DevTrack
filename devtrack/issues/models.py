import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

REPORTERS_FILE = BASE_DIR / 'reporters.json'
ISSUES_FILE = BASE_DIR / 'issues.json'

class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }

class Reporter(BaseEntity):
    def __init__(self, id, name, email, team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not self.name:
            raise ValueError('Name cannot be empty')
        if not isinstance(self.email, str) or '@' not in self.email or '.' not in self.email:
            raise ValueError('Invalid email')

class Issue(BaseEntity):
    VALID_STATUSES = {'open', 'in_progress', 'resolved', 'closed'}
    VALID_PRIORITIES = {'low', 'medium', 'high', 'critical'}

    def __init__(self, id, title, description, status, priority, reporter_id, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id
        self.created_at = created_at or str(datetime.now())

    def validate(self):
        if not self.title:
            raise ValueError('Title cannot be empty')
        if self.status not in self.VALID_STATUSES:
            raise ValueError('Invalid status')
        if self.priority not in self.VALID_PRIORITIES:
            raise ValueError('Invalid priority')
        if not isinstance(self.reporter_id, int):
            raise ValueError('Invalid reporter_id')

    def describe(self):
        return f"{self.title} [{self.priority}]"

class CriticalIssue(Issue):
    def describe(self):
        return f"[URGENT] {self.title} — needs immediate attention"

class LowPriorityIssue(Issue):
    def describe(self):
        return f"{self.title} — low priority, handle when free"


def load_json_file(path):
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

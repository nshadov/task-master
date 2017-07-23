"""Represent Task to be processed."""


class Task(object):
    """Task to be performed in backend."""

    def __init__(self, owner):
        """Create valid empty Task."""
        self._set_id()
        self._set_creation_ts()
        self.set_owner(owner)
        self.title = None
        self.desc = None

    def _set_id(self, id=None):
        """Set new ID."""
        if id is None:
            import uuid
            self.id = str(uuid.uuid4())
        else:
            self.id = id

    def get_id(self):
        """Return ID."""
        return self.id

    def _set_creation_ts(self):
        import time
        self.created_at = int(time.time())

    def get_created_date(self):
        """Return date when Task has been created."""
        return self.created_at

    def set_title(self, title):
        """Set Task title."""
        self.title = title

    def get_title(self):
        """Return Task title."""
        return self.title

    def set_description(self, desc):
        """Set Task description."""
        self.desc = desc

    def get_description(self):
        """Get Task description."""
        return self.desc

    def set_owner(self, owner):
        """Set Task owner."""
        self.owner = owner

    def get_owner(self):
        """Get Task owner."""
        return self.owner

    def as_dict(self):
        """Return object representation as dict."""
        return {
            "id": self.get_id(),
            "timestamp": self.get_created_date(),
            "owner": self.get_owner(),
            "title": self.get_title(),
            "description": self.get_description()
            }

    def from_dict(self, d):
        """Create object from dict."""
        if "id" in d:
            self._set_id(d["id"])
        if "owner" in d:
            self.set_owner(d["owner"])
        if "timestamp" in d:
            self.created_at = int(d["timestamp"])
        if "title" in d:
            self.set_title(d["title"])
        if "description" in d:
            self.set_description(d["description"])

    def __str__(self):
        """Return human readable representation of Task."""
        return "[%s..%s] %s" % (self.id[:4], self.id[-2:], self.title)

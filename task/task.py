class Task(object):
    """Task to be performed in backend."""

    def __init__(self):
        """Create valid empty object."""
        self._set_id()

    def _set_id(self, id=None):
        """Set new random ID."""
        if id is None:
            import uuid
            self.id = str(uuid.uuid4())
        else:
            self.id = id

    def get_id(self):
        """Return ID."""
        return self.id

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_description(self, desc):
        self.desc = desc

    def get_description(self):
        return self.desc

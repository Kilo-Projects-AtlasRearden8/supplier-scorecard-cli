"""Local JSON storage for suppliers."""

import json
from pathlib import Path

from .models import Supplier


class Storage:
    """Reads/writes the supplier roster to a local JSON file."""

    def __init__(self, path="suppliers.json"):
        self.path = Path(path)

    def load(self):
        """Return the list of suppliers (empty list if file missing/invalid)."""
        if not self.path.exists():
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Supplier.from_dict(d) for d in data]

    def save(self, suppliers):
        """Persist the supplier roster to the JSON file."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in suppliers], f, indent=2)

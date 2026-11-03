"""Data models for suppliers and lead-time records."""

from dataclasses import dataclass, field, asdict


def validate_quality(value: float) -> float:
    """Validate quality is in range 1-5."""
    q = float(value)
    if q < 1.0 or q > 5.0:
        raise ValueError(f"Quality must be between 1 and 5, got {q}")
    return q


@dataclass
class LeadTimeRecord:
    """A single observed lead time for a supplier."""

    date: str
    quoted_days: int
    actual_days: int
    reference: str = ""

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return LeadTimeRecord(
            date=d["date"],
            quoted_days=int(d["quoted_days"]),
            actual_days=int(d["actual_days"]),
            reference=d.get("reference", ""),
        )


@dataclass
class Supplier:
    """A resale supplier with price, speed, and quality attributes."""

    id: str
    name: str
    price: float
    quoted_lead_time: int
    quality: float
    lead_times: list = field(default_factory=list)
    notes: str = ""

    def __post_init__(self):
        """Validate quality range after initialization."""
        object.__setattr__(self, "quality", validate_quality(self.quality))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quoted_lead_time": self.quoted_lead_time,
            "quality": self.quality,
            "lead_times": [lt.to_dict() for lt in self.lead_times],
            "notes": self.notes,
        }

    @staticmethod
    def from_dict(d):
        return Supplier(
            id=d["id"],
            name=d["name"],
            price=float(d["price"]),
            quoted_lead_time=int(d["quoted_lead_time"]),
            quality=float(d["quality"]),
            lead_times=[LeadTimeRecord.from_dict(x) for x in d.get("lead_times", [])],
            notes=d.get("notes", ""),
        )

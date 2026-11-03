"""Scoring logic: normalized 0-100 scores for price, speed, and quality."""

from dataclasses import dataclass
from typing import Iterable, List, Optional

from .models import Supplier

DEFAULT_WEIGHTS = {"price": 0.40, "speed": 0.35, "quality": 0.25}


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _linear_score(value: float, best: float, worst: float, higher_is_better: bool) -> float:
    """Normalize a value to 0-100 relative to best/worst in a cohort.

    When best == worst every supplier gets 100 for that criterion.
    """
    if worst == best:
        return 100.0
    if higher_is_better:
        raw = (value - best) / (worst - best)
    else:
        raw = (worst - value) / (worst - best)
    return _clamp(raw * 100.0)


@dataclass
class ScoredSupplier:
    supplier: Supplier
    price_score: float
    speed_score: float
    quality_score: float
    overall_score: float
    rank: int = 0


def score_suppliers(
    suppliers: Iterable[Supplier], weights: Optional[dict] = None
) -> List[ScoredSupplier]:
    """Score and rank a cohort of suppliers.

    Each criterion is normalized 0-100 against the cohort, then combined
    with the given weights (default: price 40%, speed 35%, quality 25%).
    Returns a list sorted by overall score descending, with ranks assigned.
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
    suppliers = list(suppliers)
    if not suppliers:
        return []

    prices = [s.price for s in suppliers]
    lead_times = [s.quoted_lead_time for s in suppliers]
    qualities = [s.quality for s in suppliers]

    min_price, max_price = min(prices), max(prices)
    min_lead, max_lead = min(lead_times), max(lead_times)
    min_qual, max_qual = min(qualities), max(qualities)

    results = []
    for s in suppliers:
        price_score = _linear_score(s.price, min_price, max_price, higher_is_better=False)
        speed_score = _linear_score(
            s.quoted_lead_time, min_lead, max_lead, higher_is_better=False
        )
        quality_score = _linear_score(s.quality, min_qual, max_qual, higher_is_better=True)
        overall = (
            weights.get("price", 0.40) * price_score
            + weights.get("speed", 0.35) * speed_score
            + weights.get("quality", 0.25) * quality_score
        )
        results.append(
            ScoredSupplier(s, price_score, speed_score, quality_score, overall)
        )

    results.sort(key=lambda r: r.overall_score, reverse=True)
    for i, r in enumerate(results, start=1):
        r.rank = i
    return results


def score_supplier(
    supplier: Supplier, suppliers: Iterable[Supplier], weights: Optional[dict] = None
) -> ScoredSupplier:
    """Score a single supplier within the context of a cohort."""
    cohort = [s for s in suppliers if s.id != supplier.id]
    return score_suppliers([supplier] + cohort, weights)[0]

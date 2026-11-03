"""CSV export for scored suppliers."""

import csv

from .scoring import score_suppliers


def export_csv(suppliers, path="suppliers.csv", weights=None):
    """Export ranked supplier scores to a CSV file."""
    scored = score_suppliers(suppliers, weights)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "rank",
                "id",
                "name",
                "price",
                "quoted_lead_time",
                "quality",
                "price_score",
                "speed_score",
                "quality_score",
                "overall_score",
            ]
        )
        for r in scored:
            s = r.supplier
            writer.writerow(
                [
                    r.rank,
                    s.id,
                    s.name,
                    f"{s.price:.2f}",
                    s.quoted_lead_time,
                    f"{s.quality:.1f}",
                    f"{r.price_score:.2f}",
                    f"{r.speed_score:.2f}",
                    f"{r.quality_score:.2f}",
                    f"{r.overall_score:.2f}",
                ]
            )
    return scored

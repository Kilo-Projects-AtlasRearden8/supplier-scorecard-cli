"""Tests for the supplier scoring logic."""

import unittest

from supplier_scorecard.models import Supplier
from supplier_scorecard.scoring import score_suppliers, DEFAULT_WEIGHTS


def mk(sid, name, price, lead_time, quality):
    return Supplier(id=sid, name=name, price=price, quoted_lead_time=lead_time, quality=quality)


class TestScoring(unittest.TestCase):
    def test_lowest_price_gets_best_price_score(self):
        suppliers = [mk("a", "Cheap", 10.0, 5, 3), mk("b", "Pricey", 20.0, 5, 3)]
        results = score_suppliers(suppliers)
        self.assertEqual(results[0].supplier.name, "Cheap")
        self.assertEqual(results[0].price_score, 100.0)
        self.assertEqual(results[1].price_score, 0.0)

    def test_lowest_lead_time_gets_best_speed_score(self):
        suppliers = [mk("a", "Fast", 10.0, 3, 3), mk("b", "Slow", 10.0, 10, 3)]
        results = score_suppliers(suppliers)
        self.assertEqual(results[0].supplier.name, "Fast")
        self.assertEqual(results[0].speed_score, 100.0)
        self.assertEqual(results[1].speed_score, 0.0)

    def test_highest_quality_gets_best_quality_score(self):
        suppliers = [mk("a", "Poor", 10.0, 5, 1), mk("b", "Great", 10.0, 5, 5)]
        results = score_suppliers(suppliers)
        self.assertEqual(results[0].supplier.name, "Great")
        self.assertEqual(results[0].quality_score, 100.0)
        self.assertEqual(results[1].quality_score, 0.0)

    def test_quality_bounds_one_is_zero_five_is_hundred(self):
        suppliers = [mk("a", "Low", 10.0, 5, 1), mk("b", "High", 10.0, 5, 5)]
        results = score_suppliers(suppliers)
        quality_map = {r.supplier.name: r.quality_score for r in results}
        self.assertEqual(quality_map["Low"], 0.0)
        self.assertEqual(quality_map["High"], 100.0)

    def test_all_identical_suppliers_get_100_everywhere(self):
        suppliers = [mk("a", "Twin", 10.0, 5, 3), mk("b", "Twin", 10.0, 5, 3)]
        results = score_suppliers(suppliers)
        for r in results:
            self.assertEqual(r.price_score, 100.0)
            self.assertEqual(r.speed_score, 100.0)
            self.assertEqual(r.quality_score, 100.0)
            self.assertEqual(r.overall_score, 100.0)

    def test_default_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(DEFAULT_WEIGHTS.values()), 1.0)

    def test_overall_score_is_weighted_average(self):
        suppliers = [mk("a", "A", 10.0, 3, 5), mk("b", "B", 20.0, 10, 1)]
        results = score_suppliers(suppliers)
        r = results[0]
        expected = (
            0.40 * r.price_score + 0.35 * r.speed_score + 0.25 * r.quality_score
        )
        self.assertAlmostEqual(r.overall_score, expected)

    def test_ranking_is_strict_descending(self):
        suppliers = [
            mk("a", "Best", 10.0, 3, 5),
            mk("b", "Middle", 15.0, 6, 3),
            mk("c", "Worst", 20.0, 10, 1),
        ]
        results = score_suppliers(suppliers)
        names = [r.supplier.name for r in results]
        self.assertEqual(names, ["Best", "Middle", "Worst"])
        self.assertEqual([r.rank for r in results], [1, 2, 3])

    def test_empty_cohort_returns_empty(self):
        self.assertEqual(score_suppliers([]), [])


if __name__ == "__main__":
    unittest.main()

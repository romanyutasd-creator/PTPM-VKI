import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from delivery_service import calculate_delivery_cost

class TestDeliveryCost(unittest.TestCase):

    def test_weight_below_minimum(self):
        cost, _ = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_weight_above_maximum(self):
        cost, _ = calculate_delivery_cost(51.0, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_below_minimum(self):
        cost, _ = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_above_maximum(self):
        cost, _ = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_package_type(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "экзотический")
        self.assertEqual(cost, -1)

    def test_base_cost_for_minimal_order(self):
        cost, _ = calculate_delivery_cost(1.0, 1, "обычный")
        self.assertEqual(cost, 205)

    def test_fragile_adds_300(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_adds_1000(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)

    def test_express_should_be_more_expensive(self):
        normal_cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=False)
        express_cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, normal_cost, "Срочная доставка должна стоить дороже")

    def test_express_short_distance_not_zero_days(self):
        _, express_date = calculate_delivery_cost(1.0, 300, "обычный", is_express=True)
        self.assertGreater(express_date, "2026-09-03", "Экспресс не может быть в день отправки")

if __name__ == "__main__":
    unittest.main()
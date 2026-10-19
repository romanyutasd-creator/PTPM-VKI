import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from my_project import process_triangle

class TestTriangle(unittest.TestCase):

    def test_equilateral_triangle_returns_correct_type(self):
        triangle_type, _ = process_triangle("3", "4", "5")
        self.assertEqual(triangle_type, "разносторонний")

    def test_equilateral_all_sides_equal(self):
        triangle_type, _ = process_triangle("5", "5", "5")
        self.assertEqual(triangle_type, "равносторонний")

    def test_isosceles_triangle(self):
        triangle_type, _ = process_triangle("5", "5", "8")
        self.assertEqual(triangle_type, "равнобедренный")

    def test_not_triangle_by_inequality(self):
        triangle_type, coords = process_triangle("1", "2", "10")
        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side_returns_invalid_numeric(self):
        _, coords = process_triangle("-3", "4", "5")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_zero_side_returns_invalid_numeric(self):
        _, coords = process_triangle("0", "4", "5")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_non_numeric_input_returns_empty_type(self):
        triangle_type, coords = process_triangle("abc", "4", "5")
        self.assertEqual(triangle_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_valid_triangle_returns_three_vertices(self):
        _, coords = process_triangle("3", "4", "5")
        self.assertEqual(len(coords), 3)

    def test_coordinates_within_canvas(self):
        _, coords = process_triangle("3", "4", "5")
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_coordinates_are_integers(self):
        _, coords = process_triangle("3", "4", "5")
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

if __name__ == "__main__":
    unittest.main()
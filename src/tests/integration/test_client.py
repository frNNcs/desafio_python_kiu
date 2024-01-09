import unittest
from datetime import datetime

from project.models.cargo import get_total_shipments, total_collected_per_day


class TestTotalShipments(unittest.TestCase):
    def test_total_shipments(self):
        self.assertEqual(get_total_shipments(), 0)


class TestTotalCollectedPerDay(unittest.TestCase):
    def setUp(self):
        self.date_string = "2021-08-01"
        self.date_obj = datetime.strptime(self.date_string, "%Y-%m-%d").date()

    def test_total_collected_per_day(self):
        self.assertEqual(total_collected_per_day(self.date_string), 0)
        self.assertEqual(total_collected_per_day(self.date_obj), 0)

    def test_total_collected_per_day_bad_date(self):
        with self.assertRaises(Exception) as context:
            total_collected_per_day("12d12d")
        self.assertEqual(
            "Invalid date format, must be YYYY-MM-DD", str(context.exception)
        )

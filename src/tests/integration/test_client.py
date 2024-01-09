import unittest
from datetime import datetime

from project.models.cargo import get_total_shipments, total_collected_per_day


class TestTotalShipments(unittest.TestCase):
    def test_total_shipments(self):
        self.assertEqual(get_total_shipments(), 0)


class TestTotalCollectedPerDay(unittest.TestCase):
    def test_total_collected_per_day(self):
        date_string = "2021-08-01"
        date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
        self.assertEqual(total_collected_per_day(date_string), 0)
        self.assertEqual(total_collected_per_day(date_obj), 0)

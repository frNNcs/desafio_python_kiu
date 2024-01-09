import unittest
from datetime import datetime

from project.models.cargo import Shipment


class TestTotalShipments(unittest.TestCase):
    def setUp(self):
        self.date_obj = datetime.now().date()

    def test_total_shipments(self):
        self.assertGreaterEqual(Shipment.get_total_shipments_per_day(self.date_obj), 0)


class TestTotalCollectedPerDay(unittest.TestCase):
    def setUp(self):
        self.date_string = datetime.now().strftime("%Y-%m-%d")
        self.date_obj = datetime.now().date()

    def test_total_collected_per_day(self):
        self.assertGreaterEqual(Shipment.get_ammount_per_day(self.date_string), 0)
        self.assertGreaterEqual(Shipment.get_ammount_per_day(self.date_obj), 0)

    def test_total_collected_per_day_bad_date(self):
        random_strings = "12d12d"
        with self.assertRaises(Exception) as context:
            Shipment.get_ammount_per_day(random_strings)
        self.assertEqual(
            f"time data '{random_strings}' does not match format '%Y-%m-%d'",
            str(context.exception),
        )

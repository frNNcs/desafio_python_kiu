import unittest

from project.models.cargo import Package
from project.models.client import Client


class TestPackage(unittest.TestCase):
    def setUp(self):
        self.package = Package(
            description="Test package",
            type_package="Big metal box",
            weight=10.0,
            size=(10, 10, 10),
        )
        self.package.save()

    def test_package_has_description(self):
        self.assertEqual(self.package.description, "Test package")

    def test_package_has_type(self):
        self.assertEqual(self.package.type_package, "Big metal box")

    def test_package_has_weight(self):
        self.assertEqual(self.package.weight, 10.0)

    def test_package_has_size(self):
        self.assertEqual(self.package.size, (10, 10, 10))

    def test_get_package_dict(self):
        self.assertEqual(
            self.package.__dict__(),
            {
                "id": self.package.id,
                "created_at": self.package.created_at,
                "description": "Test package",
                "type_package": "Big metal box",
                "weight": 10.0,
                "size": (10, 10, 10),
            },
        )


class TestShipment(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            name="Test Client",
            email="d21d@21d21d12d",
            phone="123123123",
            address="Test Address",
            is_active=True,
        )
        self.client.save()
        self.client2 = Client(
            name="Test Destination",
            email="12d@21d21d12d",
            phone="123123123",
            address="Test Address",
            is_active=True,
        )
        self.client2.save()
        self.package = Package(
            description="Test package",
            type_package="Big metal box",
            weight=10.0,
            size=(10, 10, 10),
        )
        self.package.save()

    def test_get_shipment_dict(self):
        shipment = self.client.send_package(
            destination=self.client2,
            package=self.package,
        )
        self.assertEqual(
            shipment.__dict__(),
            {
                "id": shipment.id,
                "source": self.client.__dict__(),
                "package": self.package.__dict__(),
                "destination": self.client2.__dict__(),
                "state": shipment.state,
                "price": 10,
                "created_at": shipment.created_at,
            },
        )

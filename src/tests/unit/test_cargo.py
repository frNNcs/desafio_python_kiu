import unittest

from project.models.cargo import Package, Shipment
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

    def test_package_less_than_400kg(self):
        with self.assertRaises(Exception) as context:
            Package(
                description="Test package",
                type_package="Big metal box",
                weight=400.1,
                size=(10, 10, 10),
            )
        self.assertEqual("Package too heavy", str(context.exception))

    def test_invalid_size(self):
        with self.assertRaises(Exception) as context:
            Package(
                description="Test package",
                type_package="Big metal box",
                weight=10.0,
                size=(10, 10),
            )
        self.assertEqual("(10, 10) is an invalid size", str(context.exception))

    def test_can_delete_package(self):
        self.package.delete()
        with self.assertRaises(Exception) as context:
            Package.get_by_id(self.package.id)
        self.assertEqual("Package not found", str(context.exception))

    def test_package_too_big(self):
        with self.assertRaises(Exception) as context:
            Package(
                description="Test package",
                type_package="Big metal box",
                weight=10.0,
                size=(345, 211, 320),
            )
        self.assertEqual("PACKAGE TOO BIG", str(context.exception))


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

    def test_can_delete_shipment(self):
        shipment = self.client.send_package(self.client2, self.package)
        shipment.delete()
        with self.assertRaises(Exception) as context:
            Shipment.get_by_id(shipment.id)  # type: ignore
        self.assertEqual("Shipment not found", str(context.exception))

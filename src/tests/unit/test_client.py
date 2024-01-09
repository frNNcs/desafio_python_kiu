import unittest

from project.models.cargo import SHIPMENT_STATES, Package
from project.models.client import Client


class TestClient(unittest.TestCase):
    """Test the Client model"""

    def setUp(self):
        """Setup the test"""
        self.client = Client(
            name="Test Client",
            email="pablito@asdasd.com",
            phone="123123123",
            address="Test Address",
            is_active=True,
        )

    def test_client_has_name(self):
        """Test that the client has a name"""
        self.assertEqual(self.client.name, "Test Client")

    def test_client_has_email(self):
        """Test that the client has an email"""
        self.assertEqual(self.client.email, "pablito@asdasd.com")

    def test_client_shipments(self):
        """Test that the client has shipments"""
        self.assertEqual(self.client.shipments, [])

    def test_client_can_send_package(self):
        """Test that the client can send a package"""
        shipment = self.client.send_package(
            destination=Client(
                name="Test Destination",
                email="12d@21d21d12d",
                phone="123123123",
                address="Test Address",
                is_active=True,
            ),
            package=Package(
                description="Test package",
                type_package="Test type",
                weight=10.0,
                size=(10, 10, 10),
            ),
        )
        self.assertEqual(shipment.state, SHIPMENT_STATES.PICKUP)

    def test_not_client_canot_send_package(self):
        """Test that the client that is disabled can't send a package."""

        # Deactivate the client for this test
        self.client.is_active = False

        with self.assertRaises(Exception) as context:
            self.client.send_package(
                destination=Client(
                    name="Test Destination",
                    email="12d@21d21d12d",
                    phone="123123123",
                    address="Test Address",
                    is_active=True,
                ),
                package=Package(
                    description="Test package",
                    type_package="Test type",
                    weight=10.0,
                    size=(10, 10, 10),
                ),
            )
        self.assertTrue("Client is not a valid client", str(context.exception))

    def test_client_canot_send_package_to_itself(self):
        """Test that the client can't send a package to itself."""

        with self.assertRaises(Exception) as context:
            self.client.send_package(
                destination=self.client,
                package=Package(
                    description="Test package",
                    type_package="Test type",
                    weight=10.0,
                    size=(10, 10, 10),
                ),
            )
        self.assertTrue("Can't send a package to itself.", str(context.exception))

    def test_get_client_dict(self):
        """Test that the client can be converted to a dict"""
        self.assertEqual(
            self.client.__dict__(),
            {
                "id": self.client.id,
                "created_at": self.client.created_at.strftime("%d-%m-%Y %H:%M:%S"),
                "name": "Test Client",
                "email": "pablito@asdasd.com",
                "phone": "123123123",
                "address": "Test Address",
                "is_active": True,
            },
        )


if __name__ == "__main__":
    unittest.main()

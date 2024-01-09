from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from project.models.cargo import Package

from project.models.base import BaseModel


class Client(BaseModel):
    """Model that represents a client/inactive-client"""

    name: str
    email: str
    phone: str
    address: str
    is_active: bool

    def __init__(self, name, email, phone, address, is_active):
        super().__init__()
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.is_active = is_active

    def __dict__(self):
        return {
            **super().__dict__(),
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "is_active": self.is_active,
        }

    def save(self):
        """Saves the client to the database.

        Raises:
            Exception: If the client is not active.
        """
        if not self.is_active:
            raise Exception("Can't create a client that is not active.")
        super().save()

    @property
    def shipments(self):
        """Returns all the shipments delivered the client

        Returns:
            _type_: List[Shipment]
        """
        from project.models.cargo import Shipment

        return Shipment.get_delivered_by_client(self)

    def send_package(self, destination: Client, package: Package):
        """Sends a package to a destination.

        Args:
            destination (_type_: Client): The destination of the package.
            package (_type_: Package): The package to be sent.

        Raises:
            Exception: If the client is not active.
        """
        from project.models.cargo import Shipment

        if not self.is_active:
            raise Exception("Client is not a valid client.")

        if self == destination:
            raise Exception("Can't send a package to itself.")

        shipment = Shipment(
            source=self,
            destination=destination,
            price=10,
            package=package,
        )
        shipment.save()
        return shipment

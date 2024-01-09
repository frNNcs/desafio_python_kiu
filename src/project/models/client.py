from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from project.models.cargo import Package

from datetime import datetime

from project.models.base import BaseModel


class Client(BaseModel):
    """Model that represents a client/inactive-client"""

    id: int | None = None
    name: str
    email: str
    phone: str
    address: str
    created_at: datetime
    is_active: bool

    def __init__(
        self,
        name,
        email,
        phone,
        address,
        is_active,
        id: int | None = None,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.created_at = created_at or datetime.now()
        self.is_active = is_active

    @classmethod
    def _table_name(cls):
        return "clients"

    def __dict__(self):
        return dict(
            {
                "id": self.id,
                "name": self.name,
                "email": self.email,
                "phone": self.phone,
                "address": self.address,
                "is_active": self.is_active,
                "created_at": self.created_at,
            }
        )

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

        if self.id == destination.id:
            raise Exception("Can't send a package to itself.")

        if not self.id or not destination.id or not package.id:
            raise Exception("Please save the client, destination and package first.")

        shipment = Shipment(
            source_id=self.id,
            destination_id=destination.id,
            package_id=package.id,
            price=10,
        )
        shipment.save()
        return shipment

import datetime

from project.models.base import BaseModel
from project.models.client import Client

shipmets = {}


class Package(BaseModel):
    """
    Model that represents a package
    """

    description: str
    type_package: str
    weight: float
    size: tuple

    def __init__(self, description: str, type_package: str, weight: float, size: tuple):
        super().__init__()
        self.description = description
        self.type_package = type_package
        self.weight = weight
        self.size = size

    def __dict__(self):
        return {
            **super().__dict__(),
            "description": self.description,
            "type_package": self.type_package,
            "weight": self.weight,
            "size": self.size,
        }


class SHIPMENT_STATES:
    """Possible shipment states
    Choices are:
        - PICKUP
        - DELIVERED
        - RETURNED
        - CANCELED
    """

    PICKUP = "Pickup"
    DELIVERED = "Delivered"
    RETURNED = "Returned"
    CANCELED = "Canceled"


class Shipment(BaseModel):
    """Model that represents a shipment"""

    source: Client
    destination: Client
    price: float
    state: str = SHIPMENT_STATES.PICKUP
    package: Package

    def __init__(
        self,
        source: Client,
        destination: Client,
        price: float,
        package: Package,
    ):
        super().__init__()
        self.source = source
        self.destination = destination
        self.price = price
        self.package = package

    def __dict__(self):
        return {
            **super().__dict__(),
            "source": self.source.__dict__(),
            "destination": self.destination.__dict__(),
            "price": self.price,
            "state": self.state,
            "package": self.package.__dict__(),
        }

    def save(self):
        shipmets[self.id] = self

    @classmethod
    def get_delivered_by_client(cls, client: Client):
        """Returns all the shipments delivered by a client

        Returns:
            _type_: list[Shipment]
        """
        return [
            shipment
            for shipment in shipmets.values()
            if shipment.source.id == client.id
            and shipment.state == SHIPMENT_STATES.DELIVERED
        ]

    @classmethod
    def get_total_shipments(cls):
        """Returns the total number of shipments

        Returns:
            _type_: int
        """
        return len(
            [
                shipment
                for shipment in shipmets.values()
                # if shipment.state == SHIPMENT_STATES.DELIVERED
            ]
        )

    @classmethod
    def total_collected_per_day(cls, date: datetime.date | str):
        """Returns the total amount collected in a given day

        Args:
            date (datetime.date | str): Date to check

        Returns:
            _type_: float
        """
        if not isinstance(date, datetime.date):
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format, must be YYYY-MM-DD")

        return sum(
            [
                shipment.price
                for shipment in shipmets.values()
                if shipment.created_at.date() == date
            ]
        )

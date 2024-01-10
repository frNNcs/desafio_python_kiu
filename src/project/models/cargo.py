from datetime import date, datetime

from project.database.connection import conn as Connection
from project.models.base import BaseModel
from project.models.client import Client


class Package(BaseModel):
    """
    Model that represents a package

    Weight is in kilograms and size is in centimeters
    Weight must be less than 400kg
    """

    id: int | None = None
    description: str
    type_package: str
    weight: float
    size: tuple
    created_at: datetime

    @classmethod
    def _table_name(cls):
        return "packages"

    def __init__(
        self,
        description: str,
        type_package: str,
        weight: float,
        size: tuple,
        id: int | None = None,
        created_at: datetime | None = None,
    ):
        if weight > 400:
            raise Exception("Package too heavy")
        if not isinstance(size, tuple):
            size = size.strip(")(").split(",")
            size = tuple([int(s) for s in size])
        if len(size) != 3:
            raise Exception(f"{size} is an invalid size")
        else:
            if (size[0] * size[1] * size[2]) > 1000000:
                raise Exception("PACKAGE TOO BIG")

        self.id = id
        self.description = description
        self.type_package = type_package
        self.weight = weight
        self.size = size
        self.created_at = created_at or datetime.now()

    def save(self):
        super().save()

    def __dict__(self):
        return dict(
            {
                "id": self.id,
                "description": self.description,
                "type_package": self.type_package,
                "weight": self.weight,
                "size": self.size,
                "created_at": self.created_at,
            }
        )


class SHIPMENT_STATES:
    """Possible shipment states
    Choices are:
        - PICKUP
        - IN_TRANSIT
        - DELIVERED
        - RETURNED
        - CANCELED
    """

    PICKUP = "Pickup"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    RETURNED = "Returned"
    CANCELED = "Canceled"


class Shipment(BaseModel):
    """Model that represents a shipment"""

    id: int | None = None
    source_id: int
    destination_id: int
    price: float
    state: str = SHIPMENT_STATES.PICKUP
    package_id: int
    created_at: datetime

    @classmethod
    def _table_name(cls):
        return "shipments"

    def __init__(
        self,
        source_id: int,
        destination_id: int,
        price: float,
        package_id: int,
        state: str = SHIPMENT_STATES.PICKUP,
        id: int | None = None,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.source_id = source_id
        self.destination_id = destination_id
        self.price = price
        self.package_id = package_id
        self.created_at = created_at or datetime.now()
        self.state = state

    @property
    def source(self):
        """Returns the source of the shipment

        Returns:
            _type_: Client
        """
        return Client.get_by_id(self.source_id)

    @property
    def destination(self):
        """Returns the destination of the shipment

        Returns:
            _type_: Client
        """
        return Client.get_by_id(self.destination_id)

    @property
    def package(self):
        """Returns the package of the shipment

        Returns:
            _type_: Package
        """
        return Package.get_by_id(self.package_id)

    def __dict__(self):
        return dict(
            {
                "id": self.id,
                "source": self.source.__dict__(),
                "destination": self.destination.__dict__(),
                "price": self.price,
                "state": self.state,
                "package": self.package.__dict__(),
                "created_at": self.created_at,
            }
        )

    def mark_as_delivered(self):
        """Marks a shipment as delivered"""
        self.state = SHIPMENT_STATES.DELIVERED
        self.save()

    def __iter__(self):
        for attr in self.__dict__():
            yield attr

    def save(self):
        super().save()

    @classmethod
    def get_delivered_by_client(cls, client: Client):
        """Returns all the shipments delivered by a client

        Returns:
            _type_: list[Shipment]
        """
        cursor = Connection.cursor()
        cursor.execute(
            f"""
                SELECT * FROM {cls._table_name()}
                WHERE source_id = {client.id}
                AND state = '{SHIPMENT_STATES.DELIVERED}';
            """
        )
        shipmets = cursor.fetchall()
        if shipmets:
            return [cls(**shipment) for shipment in shipmets]  # type: ignore
        return []

    @classmethod
    def get_ammount_per_day(cls, date_field: date | str):
        """Returns the amount collected in a given day

        Args:
            date (datetime.date): Date to check

        Returns:
            _type_: float
        """
        if isinstance(date_field, str):
            try:
                date_field = datetime.strptime(date_field, "%Y-%m-%d").date()
            except AttributeError:
                raise Exception("Invalid date")

        cursor = Connection.cursor()

        cursor.execute(
            f"""
                SELECT SUM(price) as total
                FROM {cls._table_name()}
                WHERE created_at::date = '{date_field}';
            """  # type: ignore
        )

        data = cursor.fetchone()
        if data:
            if data[0] is not None:
                return data[0]
            else:
                return 0.0
        else:
            return 0.0

    @classmethod
    def get_total_shipments_per_day(cls, date_field: date | str):
        """Returns the total number of shipments

        Args:
            date (datetime.date | str): Date to check

        Returns:
            _type_: int
        """
        if isinstance(date_field, str):
            try:
                date_field = datetime.strptime(date_field, "%Y-%m-%d").date()
            except AttributeError:
                raise Exception("Invalid date")

        return Shipment.get_count_by_date(date_field)

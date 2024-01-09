import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseModel:
    """Base model for all the models in the project"""

    _id: uuid.UUID
    created_at: datetime

    def __init__(self):
        self._id = uuid.uuid4()
        self.created_at = datetime.now()

    @property
    def id(self):
        """Returns the id of the model

        Returns:
            _type_: str
        """
        return str(self._id)

    def __dict__(self):
        return {
            "id": self.id,
            "created_at": self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
        }

    def __iter__(self):
        return iter(self.__dict__().items())

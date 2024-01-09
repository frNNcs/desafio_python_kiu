from dataclasses import dataclass
from datetime import date, datetime

from project.database.connection import conn as Connection


@dataclass
class BaseModel:
    """Base model for all the models in the project"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __dict__(self):
        return self.__dict__

    def __str__(self) -> str:
        return str(self.__dict__())

    def __repr__(self) -> str:
        return str(self.__dict__())

    def _insert_str(self):
        """Returns the insert string for the model

        Returns:
            _type_: str
        """
        attrs = []
        values = []
        for attr in self.__dict__():  # type: ignore
            if attr in ["id"]:
                continue
            if attr in ["source", "destination", "package"]:
                attr = f"{attr}_id"
            attrs.append(attr)
            values.append(f"'{getattr(self, attr)}'")

        return f"""
            INSERT INTO {self.__class__._table_name()} ({','.join(attrs)})
            VALUES ({','.join(values)}) RETURNING id;
        """

    def save(self):
        cursor = Connection.cursor()
        query_string = self._insert_str()
        cursor.execute(query_string)  # type: ignore
        Connection.commit()
        id = cursor.fetchone()
        if id:
            self.id = id[0]
        else:
            raise Exception("Error saving the model")

    @classmethod
    def get_by_id(cls, id: int):
        """Returns a model by its id

        Args:
            id (int): The id of the model

        Returns:
            _type_: BaseModel
        """
        cursor = Connection.cursor()
        cursor.execute(
            f"""
                SELECT * FROM {cls._table_name()}
                WHERE id = {id};
            """  # type: ignore
        )
        data = cursor.fetchone()
        colnames = [desc[0] for desc in cursor.description]  # type: ignore

        if data:
            obj = cls(**dict(zip(colnames, data)))
            return obj
        else:
            raise Exception("Model not found")

    @classmethod
    def get_count_by_date(cls, date_field: date | str):
        """Returns the number of models in a given date"""
        if isinstance(date_field, str):
            try:
                date_field = datetime.strptime(date_field, "%Y-%m-%d").date()
            except AttributeError:
                raise Exception("Invalid date")

        cursor = Connection.cursor()
        cursor.execute(
            f"""
                SELECT COUNT(*) FROM {cls._table_name()}
                WHERE created_at::date >= '{date_field}';
            """  # type: ignore
        )
        data = cursor.fetchone()
        if data:
            return data[0]
        else:
            return 0

    @classmethod
    def _table_name(cls):
        raise NotImplementedError()

from typing import Optional

from geoalchemy2 import Geometry
from sqlmodel import Column, Field, SQLModel


class Location(SQLModel, table=True):
    __tablename__ = "locations"

    id: int = Field(default=None, primary_key=True)
    name: str
    geom: Optional[str] = Field(sa_column=Column(Geometry("POINT", srid=4326)))

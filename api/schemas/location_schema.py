from typing import Optional

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, Field, field_serializer


class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    geom: Optional[str] = Field(None, min_length=3, max_length=50)


class LocationCreate(BaseModel):
    name: str = Field(
        ...,  # berarti wajib
        min_length=3,  # minimal 3 karakter
        max_length=50,  # maksimal 50 karakter
        description="Nama harus antara 3 hingga 50 karakter.",
    )
    geom: str = Field(
        ...,  # berarti wajib
        description="Geom harus antara 3 hingga 50 karakter.",
    )


class LocationRead(BaseModel):
    id: int
    name: str
    geom: str

    @field_serializer("geom", when_used="json")
    def serialize_geom(self, value):
        if isinstance(value, WKBElement):
            return to_shape(value).wkt
        return value

    class Config:
        orm_mode = True

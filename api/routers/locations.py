import os

from auth import admin_only, superadmin_only
from database import create_db_and_tables, get_session
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from models.locations import Location
from schemas.location_schema import (
    LocationCreate,
    LocationRead,
    LocationUpdate,
)
from sqlmodel import Session, select

load_dotenv()

DUMMY_EMAIL = os.getenv("DUMMY_EMAIL")
DUMMY_PASSWORD = os.getenv("DUMMY_PASSWORD")

loc_router = APIRouter(prefix="/locations", tags=["Locations"])


@loc_router.on_event("startup")
def startup_event():
    create_db_and_tables()


@loc_router.get("/", response_model=list[LocationRead])
def get_locations(
    name: str | None = None,
    geom: str | None = None,
    session: Session = Depends(get_session),
):

    if name:
        statement = select(Location).where(Location.name.contains(name))
    else:
        statement = select(Location)

    locations = session.exec(statement).all()
    for r in locations:
        if r.geom:
            r.geom = to_shape(r.geom).wkt

    return locations


@loc_router.post("/", response_model=LocationRead)
def create_location(
    new_location: LocationCreate,
    session: Session = Depends(get_session),
    current_admin=Depends(admin_only),
):
    statement = select(Location).where(Location.name == new_location.name)
    existing_location = session.exec(statement).first()

    if existing_location:
        raise HTTPException(
            status_code=400, detail="Nama location sudah dipakai."
        )

    geo = WKTElement(new_location.geom, srid=4326)
    db_loc = Location(name=new_location.name, geom=geo)

    session.add(db_loc)
    session.commit()
    session.refresh(db_loc)

    # Convert geometry to WKT before returning
    if db_loc.geom:
        db_loc.geom = to_shape(db_loc.geom).wkt

    # Return normalized schema object
    return LocationRead.model_validate(db_loc, from_attributes=True)


@loc_router.patch("/{loc_id}")
def update_location(
    loc_id: int,
    new_data: LocationUpdate,
    session: Session = Depends(get_session),
    current_admin=Depends(admin_only),
):
    loc_data = session.get(Location, loc_id)

    if not loc_data:
        raise HTTPException(status_code=404, detail="User tidak ditemukan.")

    if new_data.name is not None:
        loc_data.name = new_data.name

    if new_data.geom is not None:
        geo = WKTElement(new_data.geom, srid=4326)
        loc_data.geom = geo

    session.add(loc_data)
    session.commit()
    session.refresh(loc_data)

    if loc_data.geom:
        loc_data.geom = to_shape(loc_data.geom).wkt

    return LocationRead.model_validate(loc_data, from_attributes=True)


@loc_router.delete("/{loc_id}")
def delete_user(
    loc_id: int,
    session: Session = Depends(get_session),
    current_admin=Depends(superadmin_only),
):
    loc_data = session.get(Location, loc_id)

    if not loc_data:
        raise HTTPException(status_code=404, detail="User tidak ditemukan.")

    session.delete(loc_data)
    session.commit()

    return {"message": f"User dengan id {loc_id} berhasil dihapus."}

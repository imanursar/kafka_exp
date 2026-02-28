import json
from typing import Optional

from database import create_db_and_tables, get_session
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
import httpx
from models.stream import (
    device_winagg_status_per2s,
    device_winagg_status_perdevice,
)
from sqlalchemy import desc
from sqlmodel import Session, select

load_dotenv()


stream_router = APIRouter(prefix="/stream", tags=["stream"])


@stream_router.on_event("startup")
def startup_event():
    create_db_and_tables()


@stream_router.get("/raw")
async def get_device_window(limit: int = 10, device_id: str = "dev-1"):
    ksql = {
        "ksql": f"""
            SELECT *
            FROM DEVICE_WINAGG_STATUS_PER2S
            WHERE DEVICE_ID = '{device_id}'
            EMIT CHANGES
            LIMIT {limit};
        """,
        "streamsProperties": {},
    }

    columns = []
    rows = []

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://ksqldb-server:8088/query",
            json=ksql,
            headers={"Content-Type": "application/json"},
        ) as resp:

            async for line in resp.aiter_lines():
                if not line:
                    continue

                obj = json.loads(line)

                # First line → schema
                if isinstance(obj, dict) and "columnNames" in obj:
                    columns = obj["columnNames"]

                # Data rows → arrays
                elif isinstance(obj, list):
                    rows.append(dict(zip(columns, obj)))

    if len(rows) == 1:
        return rows[0]

    return rows


@stream_router.get("/latest")
async def get_device():
    ksql = {
        "ksql": """
            SELECT *
            FROM DEVICE_WINAGG_STATUS_PERDEVICE;
        """,
        "streamsProperties": {},
    }

    columns = []
    rows = []

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://ksqldb-server:8088/query",
            json=ksql,
            headers={"Content-Type": "application/json"},
        ) as resp:

            async for line in resp.aiter_lines():
                if not line:
                    continue

                obj = json.loads(line)

                # First line → schema
                if isinstance(obj, dict) and "columnNames" in obj:
                    columns = obj["columnNames"]

                # Data rows → arrays
                elif isinstance(obj, list):
                    rows.append(dict(zip(columns, obj)))

    if len(rows) == 1:
        return rows[0]

    return rows


@stream_router.get("/postgresql/raw")
def get_postgresql_window(
    limit: Optional[int] = 10,
    device_id: Optional[str] = None,
    session: Session = Depends(get_session),
):

    statement = select(device_winagg_status_per2s)
    if device_id:
        statement = statement.where(
            device_winagg_status_per2s.dev_id == device_id
        )
    statement = statement.order_by(desc(device_winagg_status_per2s.EVENT_TS))

    if limit:
        statement = statement.limit(limit)

    return session.exec(statement).all()


@stream_router.get("/postgresql/latest")
def get_postgresql_window(
    device_id: Optional[str] = None,
    session: Session = Depends(get_session),
):

    statement = select(device_winagg_status_perdevice)
    if device_id:
        statement = statement.where(
            device_winagg_status_perdevice.DEVICE_ID == device_id
        )

    return session.exec(statement).all()

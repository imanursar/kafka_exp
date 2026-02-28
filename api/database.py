import json
import os

from dotenv import load_dotenv
import httpx
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
KSQLDB_URL = os.getenv("KSQLDB_URL")
KSQLDB_API_KEY = os.getenv("KSQLDB_API_KEY")
KSQLDB_API_SECRET = os.getenv("KSQLDB_API_SECRET")
HEADERS = {"Content-Type": "application/json"}

# create_engine = membuka akses ke database.
engine = create_engine(
    DATABASE_URL,
    echo=True,  # supaya query terlihat di terminal
    connect_args={"options": "-c search_path=gis_data,public"},
)

# Function untuk membuat semua tabel di database.
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


async def ksqldb_pull_query():
    ksql = {
        "ksql": f"""
            SELECT *
            FROM DEVICE_WINAGG_STATUS
            WHERE DEVICE_ID = 'dev-2'
            EMIT CHANGES
            LIMIT 10;
        """,
        "streamsProperties": {},
    }

    columns = []
    rows = []

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST", f"{KSQLDB_URL}/query", json=ksql, headers=HEADERS
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

    # Single-row query → return object
    if len(rows) == 1:
        return rows[0]

    return rows

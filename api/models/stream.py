from sqlmodel import Field, SQLModel


class stream_location(SQLModel, table=True):
    __tablename__ = "stream_location"

    id: str = Field(default=None, primary_key=True)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)
    event_ts: int = Field(nullable=False, index=True)
    device_id: str = Field(nullable=False, index=True)


class stream_status(SQLModel, table=True):
    __tablename__ = "stream_status"

    id: str = Field(default=None, primary_key=True)
    sound: float = Field(nullable=False)
    temperature: float = Field(nullable=False)
    altitude: float = Field(nullable=False)
    event_ts: int = Field(nullable=False, index=True)
    device_id: str = Field(nullable=False, index=True)


class join_events(SQLModel, table=True):
    __tablename__ = "join_events"

    id: str = Field(default=None, primary_key=True)
    id_: str = Field(default=None, nullable=False)
    sound: float = Field(nullable=False)
    temperature: float = Field(nullable=False)
    altitude: float = Field(nullable=False)
    distance: float = Field(nullable=False)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)
    event_ts: int = Field(nullable=False, index=True)
    device_id: str = Field(nullable=False, index=True)


class device_winagg_status_per2s(SQLModel, table=True):
    __tablename__ = "device_winagg_status_per2s"

    ID: str = Field(default=None, primary_key=True)
    dev_id: str = Field(nullable=False)
    EVENT_COUNT: int = Field(nullable=False)
    AVG_TEMP: float = Field(nullable=False)
    AVG_SOUND: float = Field(nullable=False)
    AVG_ALT: float = Field(nullable=False)
    LATITUDE: float = Field(nullable=False)
    LONGITUDE: float = Field(nullable=False)
    DISTANCE: float = Field(nullable=False)
    EVENT_TS: int = Field(nullable=False, index=True)
    # device_id: str = Field(nullable=False, index=True)


class device_winagg_status_perdevice(SQLModel, table=True):
    __tablename__ = "device_winagg_status_perdevice"

    DEVICE_ID: str = Field(nullable=False, primary_key=True)
    TEMPERATURE: float = Field(nullable=False)
    SOUND: float = Field(nullable=False)
    ALTITUDE: float = Field(nullable=False)
    LATITUDE: float = Field(nullable=False)
    LONGITUDE: float = Field(nullable=False)
    DISTANCE: float = Field(nullable=False)
    EVENT_TS: int = Field(nullable=False, index=True)

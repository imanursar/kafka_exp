from pydantic import BaseModel


class StreamRead(BaseModel):
    id: str
    sound: float
    temperature: float
    event_count: float
    avg_temp: float
    avg_sound: float
    avg_alt: float
    event_ts: int
    device_id: str

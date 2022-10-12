from pydantic import BaseModel


class Crime(BaseModel):
    # because of small data loss some coordinates may have None value
    latitude: float | None
    longitude: float | None

from pydantic import BaseModel

class Crime(BaseModel):
    latitude: float | None
    longitude: float | None

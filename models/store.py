from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class Store(BaseModel):
    id: Optional[str] = None
    userID: str
    name: str
    description: Optional[str] = None
    rating: Optional[float] = 0.0
    logoURL: Optional[HttpUrl] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

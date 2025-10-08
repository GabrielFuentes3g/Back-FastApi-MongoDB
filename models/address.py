from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    id: Optional[str] = None
    userid: str
    street: str
    city: str
    state: str
    postalCode: str
    country: str

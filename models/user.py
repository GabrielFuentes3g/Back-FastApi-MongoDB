from datetime import datetime
from email.headerregistry import Address
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: Optional[str] = None
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    role: Optional[str] = "customer"
    addresses: Optional[List[Address]] = []
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
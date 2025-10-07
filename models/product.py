from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Product(BaseModel):
    id: Optional[str] = None
    storeid: Optional[str] = None
    name: str                   # obligatorio
    description: Optional[str] = None
    price: float                # obligatorio
    stockQuantity: Optional[int] = 0
    category: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

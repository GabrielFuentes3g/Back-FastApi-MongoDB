from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Product(BaseModel):
    id: Optional[str] = None
    storeid: Optional[str] = None
    name: str                   
    description: Optional[str] = None
    price: float                
    stockQuantity: Optional[int] = 0
    categories: Optional[List[str]] = []
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

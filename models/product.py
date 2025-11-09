from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List, Optional

class Product(BaseModel):
    id: Optional[str] = None
    storeId: str
    name: str                   
    description: Optional[str] = None
    price: float                
    stockQuantity: Optional[int] = 0
    categoriesId: Optional[List[str]] = []
    imageURL: Optional[HttpUrl] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class OrderItem(BaseModel):
    productid: str
    name: str
    price: float
    quantity: int
    subtotal: float

class Order(BaseModel):
    id: Optional[str] = None
    userid: str
    orderDate: datetime
    status: str  
    totalAmount: float
    items: List[OrderItem]
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

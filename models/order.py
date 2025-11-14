from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from models.orderItem import OrderItem

class Order(BaseModel):
    id: Optional[str] = None
    userId: str
    orderDate: datetime
    status: str
    totalAmount: float
    items: List[OrderItem] = []
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

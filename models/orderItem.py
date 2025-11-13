from pydantic import BaseModel
from typing import Optional

class OrderItem(BaseModel):
    id: Optional[str] = None
    productId: str
    name: str
    price: float
    quantity: int
    subtotal: float
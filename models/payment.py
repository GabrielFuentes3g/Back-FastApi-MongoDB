from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Payment(BaseModel):
    id: Optional[str] = None
    orderid: str
    paymentMethod: str  # debito, credito, paypal, etc.
    paymentDate: datetime
    amount: float
    status: Optional[str] = "completed"

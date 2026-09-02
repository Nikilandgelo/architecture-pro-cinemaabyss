from datetime import datetime

from pydantic import BaseModel


class PaymentPayload(BaseModel):
    payment_id: int
    user_id: int
    amount: float
    status: str
    timestamp: datetime
    method_type: str

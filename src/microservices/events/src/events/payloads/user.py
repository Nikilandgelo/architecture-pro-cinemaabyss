from datetime import datetime

from pydantic import BaseModel


class UserPayload(BaseModel):
    user_id: int
    username: str
    action: str
    timestamp: datetime

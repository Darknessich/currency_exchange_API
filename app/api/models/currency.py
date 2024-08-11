import datetime
from pydantic import BaseModel, Field


class Convert(BaseModel):
    amount: float = 1.0
    currency_from: str = Field(pattern="[A-Z]{3,3}")
    currency_to: str = Field(pattern="[A-Z]{3,3}")
    date: datetime.date | None = None
    result: float | None = None

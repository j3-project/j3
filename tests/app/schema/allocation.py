from datetime import datetime
from typing import Optional

from j3.schema import BaseModel


class BatchAddSchema(BaseModel):
    eta: Optional[datetime]
    ref: str
    sku: str
    qty: int


class BatchDelete(BaseModel):
    eta: Optional[datetime]
    refs: list[str]
    sku: str
    qty: int


class BatchAllocateSchema(BaseModel):
    eta: Optional[datetime]
    orderid: str
    sku: str
    qty: int

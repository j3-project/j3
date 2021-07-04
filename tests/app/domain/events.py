from dataclasses import dataclass

from j3.core import Event


@dataclass
class OutOfStock(Event, Exception):
    sku: str


@dataclass
class Allocated(Event):
    orderid: str
    sku: str
    qty: int
    batchref: str


@dataclass
class Deallocated(Event):
    orderid: str
    sku: str
    qty: int

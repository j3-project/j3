from __future__ import annotations

from typing import Optional

from j3.core import Aggregate
from j3.logging import get_logger
from tests.app.domain import commands, events
from tests.app.domain.models import Batch, OrderLine

logger = get_logger("tests.app.domain")


class Product(Aggregate[Batch]):
    def __init__(self, sku: str, items: list[Batch], version_number: int = 0):
        self.id = sku  # Entity 프로토콜을 준수하기 위해 반드시 정의해야 하는 속성.
        self.sku = sku
        self.items = items
        self.version_number = version_number

    def allocate(self, line: OrderLine) -> Optional[str]:
        try:
            if not self.items:
                raise StopIteration
            batch = next(b for b in sorted(self.items) if b.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1
            self.messages.append(
                events.Allocated(
                    orderid=line.orderid,
                    sku=line.sku,
                    qty=line.qty,
                    batchref=batch.reference,
                )
            )
            logger.info(
                "allocate batch: %r, avail_qty=%d, allocations=%r",
                batch.reference,
                batch.available_quantity,
                batch._allocations,
            )
            return batch.reference
        except StopIteration:
            self.add_message(events.OutOfStock(line.sku))
            return None

    def reallocate(self, line: OrderLine) -> Optional[str]:
        """기존 Sku의 주문선을 할당 해재 후 새로운 `line`을 할당합니다.

        재할당 서비스 함수의 경우, 작업중 예외가 발생하면 UoW의 동작 방식에 의해 이전 상태로 자동 롤백됩니다.
        모든 유효성 검사와 세부 작업이 다 성공할 경우에만 명시적으로 호출된 commit 함수에 의해 저장소 내용이 변경됩니다.
        """
        try:
            batch = next(b for b in sorted(self.items) if b.can_allocate(line))
            batch.deallocate(line)
            batch.allocate(line)
            return batch.reference
        except StopIteration:
            self.add_message(events.OutOfStock(line.sku))
            return None

    def change_batch_quantity(self, ref: str, new_qty: int) -> None:
        """배치에 할당된 주문선을 수량만큼 해제합니다."""
        batch = next(b for b in self.items if b.reference == ref)
        batch._purchased_quantity = new_qty
        logger.info(
            "change_batch_quantity: ref=%r, new_qty=%r, avail_qty=%r",
            ref,
            new_qty,
            batch.available_quantity,
        )
        while batch.available_quantity < 0:
            line = batch.deallocate_one()
            if line:
                self.messages.append(
                    commands.Allocate(line.orderid, line.sku, line.qty)
                )
                self.messages.append(
                    events.Deallocated(line.orderid, line.sku, line.qty)
                )

"""FastAPI 엔드포인트 라우팅 모듈입니다."""
from __future__ import annotations

from j3.api import app
from j3.event import messagebus
from tests.app.domain import commands
from tests.app.handlers.allocation import InvalidSku
from tests.app.schema.allocation import BatchAddSchema, BatchAllocateSchema


@app.post("/batches", status_code=201)
def add_batch(batch: BatchAddSchema):
    """``POST /batches`` 요청을 처리하여 새로운 배치를 저장소에 추가합니다."""
    event = commands.CreateBatch(batch.ref, batch.sku, batch.qty, batch.eta)
    messagebus.handle(event)


@app.post("/batches/allocate", status_code=201)
def post_allocate_batch(req: BatchAllocateSchema):
    """``POST /allocate`` 엔트포인트 요청을 처리합니다."""
    try:
        event = commands.Allocate(req.orderid, req.sku, req.qty)
        results = messagebus.handle(event)
        return {"batchref": results.pop(0)}
    except InvalidSku as e:
        return {"batchref": None, "error": "InvalidSku"}

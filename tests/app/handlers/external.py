from typing import Any

from j3.core import AbstractPubsubClient
from j3.event import messagebus, on_external_msg
from tests.app.domain import commands


@on_external_msg(commands.ChangeBatchQuantity)
def on_change_batch_quantity(client: AbstractPubsubClient, data: dict[str, Any]):
    cmd = commands.ChangeBatchQuantity(ref=data["batchref"], qty=data["qty"])
    messagebus.handle(cmd)

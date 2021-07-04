"""사용자 이벤트 정의."""
from dataclasses import dataclass

from j3.core import Event


@dataclass
class SampleEvent(Event):
    "샘플 이벤트"
    msg: str

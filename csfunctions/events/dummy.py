from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class DummyEventData(BaseModel):
    documents: list[Document]
    parts: list[Part]


class DummyEvent(BaseEvent):
    """
    Dummy Event, for unit testing
    """

    def __init__(self, event_id: str, data: DummyEventData, **_):
        super().__init__(name=EventNames.DUMMY, event_id=event_id, data=data)

    name: Literal[EventNames.DUMMY]
    data: DummyEventData = Field([])

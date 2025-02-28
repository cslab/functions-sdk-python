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

    name: Literal[EventNames.DUMMY] = EventNames.DUMMY
    data: DummyEventData = Field(..., description="Dummy Event Data")

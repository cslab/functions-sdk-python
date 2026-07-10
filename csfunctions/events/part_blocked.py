from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class PartBlockedData(BaseModel):
    parts: list[Part] = Field(..., description="List of parts that were blocked.")
    documents: list[Document] = Field(..., description="List of documents that belong to the parts.")


class PartBlockedEvent(BaseEvent):
    name: Literal[EventNames.PART_BLOCKED] = EventNames.PART_BLOCKED
    data: PartBlockedData

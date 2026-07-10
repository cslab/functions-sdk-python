from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class PartIndexedData(BaseModel):
    parts: list[Part] = Field(..., description="List of parts that were indexed.")
    documents: list[Document] = Field(..., description="List of documents that are referenced by the parts.")


class PartIndexedEvent(BaseEvent):
    name: Literal[EventNames.PART_INDEXED] = EventNames.PART_INDEXED
    data: PartIndexedData

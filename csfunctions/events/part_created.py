from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class PartCreatedData(BaseModel):
    parts: list[Part] = Field(..., description="List of parts that were created.")
    documents: list[Document] = Field(..., description="List of documents that are referenced by the parts.")


class PartCreatedEvent(BaseEvent):
    name: Literal[EventNames.PART_CREATED] = EventNames.PART_CREATED
    data: PartCreatedData

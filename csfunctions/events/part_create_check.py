from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class PartCreateCheckData(BaseModel):
    parts: list[Part] = Field(..., description="List of parts that are about to be created")
    documents: list[Document] = Field(..., description="List of documents that are referenced by the parts.")


class PartCreateCheckEvent(BaseEvent):
    name: Literal[EventNames.PART_CREATE_CHECK] = EventNames.PART_CREATE_CHECK
    data: PartCreateCheckData

from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class DocumentCreatedData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that were created.")
    parts: list[Part] = Field(..., description="List of parts that belong to the documents.")


class DocumentCreatedEvent(BaseEvent):
    name: Literal[EventNames.DOCUMENT_CREATED] = EventNames.DOCUMENT_CREATED
    data: DocumentCreatedData

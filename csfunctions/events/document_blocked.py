from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class DocumentBlockedData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that were blocked.")
    parts: list[Part] = Field(..., description="List of parts that belong to the documents.")


class DocumentBlockedEvent(BaseEvent):
    name: Literal[EventNames.DOCUMENT_BLOCKED] = EventNames.DOCUMENT_BLOCKED
    data: DocumentBlockedData

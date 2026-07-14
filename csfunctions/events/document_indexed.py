from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class DocumentIndexedData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that were indexed.")
    parts: list[Part] = Field(..., description="List of parts that belong to the documents.")


class DocumentIndexedEvent(BaseEvent):
    name: Literal[EventNames.DOCUMENT_INDEXED] = EventNames.DOCUMENT_INDEXED
    data: DocumentIndexedData

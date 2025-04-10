from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class DocumentCreateCheckData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that are about to be created")
    parts: list[Part] = Field(..., description="List of parts that belong to the documents")


class DocumentCreateCheckEvent(BaseEvent):
    name: Literal[EventNames.DOCUMENT_CREATE_CHECK] = EventNames.DOCUMENT_CREATE_CHECK
    data: DocumentCreateCheckData

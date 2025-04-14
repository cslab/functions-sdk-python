from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class CustomOperationDocumentData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that the custom operation was called on")
    parts: list[Part] = Field(..., description="List of parts that belong to the documents")


class CustomOperationDocumentEvent(BaseEvent):
    """
    Event triggered when a custom operation is called on a document.
    """

    name: Literal[EventNames.CUSTOM_OPERATION_DOCUMENT] = EventNames.CUSTOM_OPERATION_DOCUMENT
    data: CustomOperationDocumentData

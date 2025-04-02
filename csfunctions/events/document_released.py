from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames
from .dialog_data import DocumentReleasedDialogData


class DocumentReleasedData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that were released.")
    parts: list[Part] = Field(..., description="List of parts that belong to the released documents")
    dialog_data: DocumentReleasedDialogData


class DocumentReleasedEvent(BaseEvent):
    name: Literal[EventNames.DOCUMENT_RELEASED] = EventNames.DOCUMENT_RELEASED
    data: DocumentReleasedData

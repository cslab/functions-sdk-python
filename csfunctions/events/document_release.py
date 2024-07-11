from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames
from .dialog_data import DocumentReleaseDialogData


class DocumentReleaseData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that were released.")
    parts: list[Part] = Field(..., description="List of parts that belong to the released documents")
    dialog_data: DocumentReleaseDialogData


class DocumentReleaseEvent(BaseEvent):
    name: Literal[EventNames.DOCUMENT_RELEASE] = EventNames.DOCUMENT_RELEASE
    data: DocumentReleaseData

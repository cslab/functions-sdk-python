from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames
from .dialog_data import DocumentReleaseDialogData


class DocumentReleaseCheckData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that will be released.")
    attached_parts: list[Part] = Field(..., description="List of parts that belong to the documents")
    dialog_data: DocumentReleaseDialogData


class DocumentReleaseCheckEvent(BaseEvent):
    name: Literal[EventNames.DOCUMENT_RELEASE_CHECK] = EventNames.DOCUMENT_RELEASE_CHECK
    data: DocumentReleaseCheckData

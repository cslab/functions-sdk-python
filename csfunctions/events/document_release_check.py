from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part
from csfunctions.subject import Subject

from .base import BaseEvent, EventNames
from .dialog_data import DocumentReleasedDialogData


class DocumentReleaseCheckData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that will be released.")
    parts: list[Part] = Field(..., description="List of parts that belong to the documents")
    dialog_data: DocumentReleasedDialogData
    reviewers: list[Subject] = Field(
        default_factory=list,
        description="List of reviewers assigned to the release. Only populated for express releases.",
    )


class DocumentReleaseCheckEvent(BaseEvent):
    name: Literal[EventNames.DOCUMENT_RELEASE_CHECK] = EventNames.DOCUMENT_RELEASE_CHECK
    data: DocumentReleaseCheckData

from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part
from csfunctions.subject import Subject

from .base import BaseEvent, EventNames
from .dialog_data import PartReleasedDialogData


class PartReleaseCheckData(BaseModel):
    parts: list[Part] = Field(..., description="List of parts that will be released.")
    documents: list[Document] = Field(..., description="List of documents that are referenced by the parts.")
    dialog_data: PartReleasedDialogData
    reviewers: list[Subject] = Field(
        default_factory=list,
        description="List of reviewers assigned to the release. Only populated for express releases.",
    )


class PartReleaseCheckEvent(BaseEvent):
    name: Literal[EventNames.PART_RELEASE_CHECK]
    data: PartReleaseCheckData

from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, EngineeringChange, Part

from .base import BaseEvent, EventNames
from .dialog_data import DocumentReleaseDialogData, PartReleaseDialogData


class ReleaseCheckData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that will be released.")
    parts: list[Part] = Field(..., description="List of parts that will be released.")
    engineering_changes: list[EngineeringChange] = Field(
        ..., description="List of engineering changes will be released."
    )
    dialog_data: DocumentReleaseDialogData | PartReleaseDialogData | None


class ReleaseCheckEvent(BaseEvent):
    name: Literal[EventNames.RELEASE_CHECK] = EventNames.RELEASE_CHECK
    data: ReleaseCheckData

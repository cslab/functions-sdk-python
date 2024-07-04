from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, EngineeringChange, Part

from .base import BaseEvent, EventNames
from .dialog_data import DocumentReleaseDialogData, PartReleaseDialogData


class ReleasedData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that have been be released.")
    parts: list[Part] = Field(..., description="List of parts that have been released.")
    engineering_changes: list[EngineeringChange] = Field(
        ..., description="List of engineering changes have been released."
    )
    dialog_data: DocumentReleaseDialogData | PartReleaseDialogData | None


class ReleasedEvent(BaseEvent):
    name: Literal[EventNames.RELEASED] = EventNames.RELEASED
    data: ReleasedData

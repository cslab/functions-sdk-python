from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames
from .dialog_data import PartReleaseDialogData


class PartReleaseCheckData(BaseModel):
    parts: list[Part] = Field(..., description="List of parts that will be released.")
    attached_documents: list[Document] = Field(..., description="List of documents that are referenced by the parts.")
    dialog_data: PartReleaseDialogData


class PartReleaseCheckEvent(BaseEvent):
    name: Literal[EventNames.PART_RELEASE_CHECK]
    data: PartReleaseCheckData

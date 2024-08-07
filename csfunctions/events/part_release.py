from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames
from .dialog_data import PartReleaseDialogData


class PartReleaseData(BaseModel):
    parts: list[Part] = Field(..., description="List if parts that were released.")
    documents: list[Document] = Field(..., description="List if documents that are referenced by the released part.")
    dialog_data: PartReleaseDialogData


class PartReleaseEvent(BaseEvent):
    name: Literal[EventNames.PART_RELEASE] = EventNames.PART_RELEASE
    data: PartReleaseData

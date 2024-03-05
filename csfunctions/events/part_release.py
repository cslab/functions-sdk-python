from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class PartReleaseDialogData(BaseModel):
    cdbprot_remark: str | None = Field("", description="remark")
    cdb_ec_id: str | None = Field("", description="Engineering Change ID")


class PartReleaseData(BaseModel):
    def __init__(self, parts: list[Part], dialog_data: dict, **kwargs):
        super().__init__(parts=parts, dialog_data=dialog_data, **kwargs)

    parts: list[Part] = Field(..., description="List if parts that were released.")
    documents: list[Document] = Field(..., description="List if documents that are referenced by the released part.")
    dialog_data: PartReleaseDialogData


class PartReleaseEvent(BaseEvent):
    def __init__(self, event_id: str, data: PartReleaseData, **_):
        super().__init__(name=EventNames.PART_RELEASE, event_id=event_id, data=data)

    name: Literal[EventNames.PART_RELEASE]
    data: PartReleaseData

from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class DocumentReleaseDialogData(BaseModel):
    cdbprot_remark: str | None = Field(None, description="remark")
    cdb_ec_id: str | None = Field(None, description="Engineering Change ID")


class DocumentReleaseData(BaseModel):
    def __init__(self, documents: list[Document], parts: list[Part], dialog_data: dict, **kwargs):
        super().__init__(documents=documents, parts=parts, dialog_data=dialog_data, **kwargs)

    documents: list[Document] = Field(..., description="List if documents that were released.")
    parts: list[Part] = Field(..., description="List of parts that belong to the released documents")
    dialog_data: DocumentReleaseDialogData


class DocumentReleaseEvent(BaseEvent):
    def __init__(self, event_id: str, data: DocumentReleaseData, **_):
        super().__init__(name=EventNames.DOCUMENT_RELEASE, event_id=event_id, data=data)

    name: Literal[EventNames.DOCUMENT_RELEASE]
    data: DocumentReleaseData

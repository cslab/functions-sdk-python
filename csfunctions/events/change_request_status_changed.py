from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import ChangeRequest, Document, Part

from .base import BaseEvent, EventNames


class ChangeRequestStatusChangedData(BaseModel):
    change_request: ChangeRequest = Field(..., description="The change request that had its status modified")
    prev_status: int = Field(..., description="The previous status of the change request")
    documents: list[Document] = Field(..., description="List of documents attached to the change request")
    parts: list[Part] = Field(..., description="List of parts attached to the change request")


class ChangeRequestStatusChangedEvent(BaseEvent):
    name: Literal[EventNames.CHANGE_REQUEST_STATUS_CHANGED] = EventNames.CHANGE_REQUEST_STATUS_CHANGED
    data: ChangeRequestStatusChangedData

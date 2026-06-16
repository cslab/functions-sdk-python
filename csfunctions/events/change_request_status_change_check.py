from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import ChangeRequest, Document, Part

from .base import BaseEvent, EventNames


class ChangeRequestStatusChangeCheckData(BaseModel):
    change_request: ChangeRequest = Field(..., description="The change request that will have its status modified")
    target_status: int = Field(..., description="The target status of the change request")
    documents: list[Document] = Field(..., description="List of documents attached to the change request")
    parts: list[Part] = Field(..., description="List of parts attached to the change request")


class ChangeRequestStatusChangeCheckEvent(BaseEvent):
    name: Literal[EventNames.CHANGE_REQUEST_STATUS_CHANGE_CHECK] = EventNames.CHANGE_REQUEST_STATUS_CHANGE_CHECK
    data: ChangeRequestStatusChangeCheckData

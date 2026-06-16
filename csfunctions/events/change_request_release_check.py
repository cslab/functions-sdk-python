from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import ChangeRequest, Document, Part

from .base import BaseEvent, EventNames


class ChangeRequestReleaseCheckData(BaseModel):
    documents: list[Document] = Field(..., description="List of included documents.")
    parts: list[Part] = Field(..., description="List of included parts.")
    change_requests: list[ChangeRequest] = Field(..., description="List of change requests that will be released.")


class ChangeRequestReleaseCheckEvent(BaseEvent):
    name: Literal[EventNames.CHANGE_REQUEST_RELEASE_CHECK] = EventNames.CHANGE_REQUEST_RELEASE_CHECK
    data: ChangeRequestReleaseCheckData

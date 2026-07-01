from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import ChangeRequest, Document, Part

from .base import BaseEvent, EventNames


class ChangeRequestReleasedData(BaseModel):
    documents: list[Document] = Field(..., description="List of included documents.")
    parts: list[Part] = Field(..., description="List of included parts.")
    change_requests: list[ChangeRequest] = Field(..., description="List of change requests that were released.")


class ChangeRequestReleasedEvent(BaseEvent):
    name: Literal[EventNames.CHANGE_REQUEST_RELEASED] = EventNames.CHANGE_REQUEST_RELEASED
    data: ChangeRequestReleasedData

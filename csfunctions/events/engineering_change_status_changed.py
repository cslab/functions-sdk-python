from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, EngineeringChange, Part

from .base import BaseEvent, EventNames


class EngineeringChangeStatusChangedData(BaseModel):
    engineering_change: EngineeringChange = Field(
        ..., description="The engineering change that had its status modified"
    )
    prev_status: int = Field(..., description="The previous status of the engineering change")
    documents: list[Document] = Field(..., description="List of documents attached to the engineering change")
    parts: list[Part] = Field(..., description="List of parts attached to the engineering change")


class EngineeringChangeStatusChangedEvent(BaseEvent):
    name: Literal[EventNames.ENGINEERING_CHANGE_STATUS_CHANGED] = EventNames.ENGINEERING_CHANGE_STATUS_CHANGED
    data: EngineeringChangeStatusChangedData

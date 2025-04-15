from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, EngineeringChange, Part

from .base import BaseEvent, EventNames


class EngineeringChangeStatusChangeCheckData(BaseModel):
    engineering_change: EngineeringChange = Field(
        ..., description="The engineering change that will have its status modified"
    )
    target_status: int = Field(..., description="The target status of the engineering change")
    documents: list[Document] = Field(..., description="List of documents attached to the engineering change")
    parts: list[Part] = Field(..., description="List of parts attached to the engineering change")


class EngineeringChangeStatusChangeCheckEvent(BaseEvent):
    name: Literal[EventNames.ENGINEERING_CHANGE_STATUS_CHANGE_CHECK] = EventNames.ENGINEERING_CHANGE_STATUS_CHANGE_CHECK
    data: EngineeringChangeStatusChangeCheckData

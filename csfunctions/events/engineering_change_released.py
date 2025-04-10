from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, EngineeringChange, Part

from .base import BaseEvent, EventNames


class EngineeringChangeReleasedData(BaseModel):
    documents: list[Document] = Field(..., description="List of included documents.")
    parts: list[Part] = Field(..., description="List of included parts.")
    engineering_changes: list[EngineeringChange] = Field(
        ..., description="List of engineering changes that were released."
    )


class EngineeringChangeReleasedEvent(BaseEvent):
    name: Literal[EventNames.ENGINEERING_CHANGE_RELEASED] = EventNames.ENGINEERING_CHANGE_RELEASED
    data: EngineeringChangeReleasedData

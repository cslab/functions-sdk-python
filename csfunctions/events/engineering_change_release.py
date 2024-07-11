from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, EngineeringChange, Part

from .base import BaseEvent, EventNames


class EngineeringChangeReleaseData(BaseModel):
    documents: list[Document] = Field(..., description="List of included documents.")
    parts: list[Part] = Field(..., description="List of included parts.")
    engineering_changes: list[EngineeringChange] = Field(
        ..., description="List of engineering changes that were released."
    )


class EngineeringChangeRelease(BaseEvent):
    name: Literal[EventNames.ENGINEERING_CHANGE_RELEASE] = EventNames.ENGINEERING_CHANGE_RELEASE
    data: EngineeringChangeReleaseData

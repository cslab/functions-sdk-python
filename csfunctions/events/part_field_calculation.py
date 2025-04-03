from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class PartFieldCalculationData(BaseModel):
    part: Part = Field(..., description="Current state of the part")
    action: Literal["create", "modify", "copy", "index"] = Field(..., description="Action being performed")

    documents: list[Document] = Field(..., description="List of documents that are referenced by the parts.")


class PartFieldCalculationEvent(BaseEvent):
    name: Literal[EventNames.PART_FIELD_CALCULATION] = EventNames.PART_FIELD_CALCULATION
    data: PartFieldCalculationData

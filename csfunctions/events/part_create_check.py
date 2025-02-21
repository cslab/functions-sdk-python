from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Part

from .base import BaseEvent, EventNames


class PartCreateCheckData(BaseModel):
    parts: list[Part] = Field(..., description="List of parts that are about to be created")
    attached_parts: list[Part] = Field(..., description="Contains the original part(s) if a part is a copy")


class PartCreateCheckEvent(BaseEvent):
    name: Literal[EventNames.PART_CREATE_CHECK] = EventNames.PART_CREATE_CHECK
    data: PartCreateCheckData

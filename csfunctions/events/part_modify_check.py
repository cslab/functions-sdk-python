from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Part

from .base import BaseEvent, EventNames


class PartModifyCheckData(BaseModel):
    parts: list[Part] = Field(..., description="List of parts that are about to be modified")


class PartModifyCheckEvent(BaseEvent):
    name: Literal[EventNames.PART_MODIFY_CHECK] = EventNames.PART_MODIFY_CHECK
    data: PartModifyCheckData

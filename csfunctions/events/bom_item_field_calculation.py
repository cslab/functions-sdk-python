from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import BOMItem, Part

from .base import BaseEvent, EventNames


class BOMItemFieldCalculationData(BaseModel):
    bom_item: BOMItem = Field(..., description="Current state of the BOM item")
    action: Literal["create", "modify", "copy", "index"] = Field(..., description="Action being performed")
    part: Part = Field(..., description="Part of the BOM item")


class BOMItemFieldCalculationEvent(BaseEvent):
    name: Literal[EventNames.BOM_ITEM_FIELD_CALCULATION] = EventNames.BOM_ITEM_FIELD_CALCULATION
    data: BOMItemFieldCalculationData

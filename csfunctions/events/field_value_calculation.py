from typing import Literal

from pydantic import BaseModel

from .base import BaseEvent, EventNames


class FieldValueCalculationData(BaseModel):
    scheme_updates: dict
    ctx: dict
    obj: dict
    old_cfv_str: str
    matches: list
    prefix: str


class FieldValueCalculationEvent(BaseEvent):
    name: Literal[EventNames.FIELD_VALUE_CALCULATION]
    data: FieldValueCalculationData

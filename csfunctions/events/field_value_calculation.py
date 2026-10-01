from typing import Literal

from pydantic import BaseModel, Field

from .base import BaseEvent, EventNames


class FieldValueCalculation(BaseModel):
    """A single field calculation, used when several calculations are sent in one event."""

    sid: str = Field(..., description="Identifier of the calculation, used to map the result.")
    attribute: str = Field(..., description="Attribute of obj that receives the calculated value.")
    scheme_updates: dict
    old_cfv_str: str
    matches: list
    prefix: str


class FieldValueCalculationData(BaseModel):
    scheme_updates: dict
    ctx: dict
    obj: dict
    old_cfv_str: str
    matches: list
    prefix: str
    calculations: list[FieldValueCalculation] | None = Field(
        None,
        description="All calculations of the object, in the order they have to be evaluated. "
        "If set, the single calculation fields above are ignored and each calculated value is "
        "written to obj before the next calculation is evaluated.",
    )


class FieldValueCalculationEvent(BaseEvent):
    name: Literal[EventNames.FIELD_VALUE_CALCULATION]
    data: FieldValueCalculationData

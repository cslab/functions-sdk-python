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
    attribute_types: dict[str, Literal["int", "float", "date"]] = Field(
        default_factory=dict,
        description="Types of the attributes of obj that are not strings, attributes of "
        "obj['Item'] as 'Item.<attribute>'. Attributes that are missing are strings. "
        "Dates are sent as ISO 8601 strings and converted "
        "to date or datetime before the calculations are evaluated. Calculated values are "
        "converted to the type of their attribute before they are written to obj, like "
        "CIM Database Cloud does when the value is set on the object; calculated dates are "
        "returned in the format DD.MM.YYYY[ HH:MM:SS].",
    )
    calculations: list[FieldValueCalculation] | None = Field(
        None,
        description="All calculations of the object, in the order they have to be evaluated. "
        "If set, the single calculation fields above are ignored and each calculated value is "
        "written to obj before the next calculation is evaluated.",
    )


class FieldValueCalculationEvent(BaseEvent):
    name: Literal[EventNames.FIELD_VALUE_CALCULATION]
    data: FieldValueCalculationData

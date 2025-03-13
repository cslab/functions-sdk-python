from datetime import datetime
from typing import Literal

from pydantic import Field

from .base import BaseObject, ObjectType


class ObjectPropertyValue(BaseObject):
    """
    An objects property, used by classification.
    """

    object_type: Literal[ObjectType.OBJECT_PROPERTY_VALUE] = ObjectType.OBJECT_PROPERTY_VALUE

    ref_object_id: str = Field(..., description="Referenced Object")
    boolean_value: int | None = Field(..., description="Boolean Value")
    datetime_value: datetime | None = Field(..., description="Datetime Value")
    float_value: float | None = Field(None, description="Float Value")
    float_value_normalized: float | None = Field(None, description="Float Value Normalized")
    integer_value: int | None = Field(None, description="Integer Value")
    iso_language_code: str | None = Field(None, description="ISO Language Code")
    value_pos: int | None = Field(None, description="Position")
    property_code: str | None = Field("", description="Property Code")
    property_path: str | None = Field(None, description="Property Path")
    property_type: str | None = Field(None, description="Property Type")
    range_identifier: str | None = Field(None, description="Range ID")
    text_value: str | None = Field(None, description="Text")

from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import ChangeOrder, Document, Part

from .base import BaseEvent, EventNames


class ChangeOrderReleasedData(BaseModel):
    documents: list[Document] = Field(..., description="List of included documents.")
    parts: list[Part] = Field(..., description="List of included parts.")
    change_orders: list[ChangeOrder] = Field(..., description="List of change orders that were released.")


class ChangeOrderReleasedEvent(BaseEvent):
    name: Literal[EventNames.CHANGE_ORDER_RELEASED] = EventNames.CHANGE_ORDER_RELEASED
    data: ChangeOrderReleasedData

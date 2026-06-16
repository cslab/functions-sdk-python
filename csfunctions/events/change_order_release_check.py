from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import ChangeOrder, Document, Part

from .base import BaseEvent, EventNames


class ChangeOrderReleaseCheckData(BaseModel):
    documents: list[Document] = Field(..., description="List of included documents.")
    parts: list[Part] = Field(..., description="List of included parts.")
    change_orders: list[ChangeOrder] = Field(..., description="List of change orders that will be released.")


class ChangeOrderReleaseCheckEvent(BaseEvent):
    name: Literal[EventNames.CHANGE_ORDER_RELEASE_CHECK] = EventNames.CHANGE_ORDER_RELEASE_CHECK
    data: ChangeOrderReleaseCheckData

from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import ChangeOrder, Document, Part

from .base import BaseEvent, EventNames


class ChangeOrderStatusChangedData(BaseModel):
    change_order: ChangeOrder = Field(..., description="The change order that had its status modified")
    prev_status: int = Field(..., description="The previous status of the change order")
    documents: list[Document] = Field(..., description="List of documents attached to the change order")
    parts: list[Part] = Field(..., description="List of parts attached to the change order")


class ChangeOrderStatusChangedEvent(BaseEvent):
    name: Literal[EventNames.CHANGE_ORDER_STATUS_CHANGED] = EventNames.CHANGE_ORDER_STATUS_CHANGED
    data: ChangeOrderStatusChangedData

from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import ChangeOrder, Document, Part

from .base import BaseEvent, EventNames


class ChangeOrderStatusChangeCheckData(BaseModel):
    change_order: ChangeOrder = Field(..., description="The change order that will have its status modified")
    target_status: int = Field(..., description="The target status of the change order")
    documents: list[Document] = Field(..., description="List of documents attached to the change order")
    parts: list[Part] = Field(..., description="List of parts attached to the change order")


class ChangeOrderStatusChangeCheckEvent(BaseEvent):
    name: Literal[EventNames.CHANGE_ORDER_STATUS_CHANGE_CHECK] = EventNames.CHANGE_ORDER_STATUS_CHANGE_CHECK
    data: ChangeOrderStatusChangeCheckData

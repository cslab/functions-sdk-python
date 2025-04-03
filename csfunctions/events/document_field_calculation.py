from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class DocumentFieldCalculationData(BaseModel):
    document: Document = Field(..., description="Current state of the document")
    action: Literal["create", "modify", "copy", "index"] = Field(..., description="Action being performed")
    parts: list[Part] = Field(..., description="Parts that belong to the document")


class DocumentFieldCalculationEvent(BaseEvent):
    name: Literal[EventNames.DOCUMENT_FIELD_CALCULATION] = EventNames.DOCUMENT_FIELD_CALCULATION
    data: DocumentFieldCalculationData

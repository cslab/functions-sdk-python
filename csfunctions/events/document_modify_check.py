from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Document, Part

from .base import BaseEvent, EventNames


class DocumentModifyCheckData(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that are about to be modified")
    parts: list[Part] = Field(..., description="List of parts that belong to the documents")


class DocumentModifyCheckEvent(BaseEvent):
    name: Literal[EventNames.DOCUMENT_MODIFY_CHECK] = EventNames.DOCUMENT_MODIFY_CHECK
    data: DocumentModifyCheckData

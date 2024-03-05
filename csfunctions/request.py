from pydantic import BaseModel, Field

from csfunctions.events import Event
from csfunctions.metadata import MetaData


class Request(BaseModel):
    metadata: MetaData = Field(..., description="General information.")
    event: Event

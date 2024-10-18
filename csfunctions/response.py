from enum import Enum
from typing import Annotated, Literal, Union
from uuid import uuid4

from pydantic import BaseModel, Field

from csfunctions.actions import Action


class ResponseType(str, Enum):
    WORKLOAD = "workload"
    DATA = "data"
    ERROR = "error"
    EMPTY = "empty"


class WorkloadResponse(BaseModel):
    def __init__(
        self,
        actions: list[Action],
        event_id: str | None = None,
        response_type: Literal[ResponseType.WORKLOAD] | None = None,  # pylint: disable=unused-argument
        **kwargs,
    ):
        event_id = event_id or str(uuid4())
        super().__init__(response_type=ResponseType.WORKLOAD, event_id=event_id, actions=actions, **kwargs)

    response_type: Literal[ResponseType.WORKLOAD]
    event_id: str = Field(..., description="")
    actions: list[Action] = Field(..., description="actions that should be performed by the elements instance")


class DataResponse(BaseModel):
    def __init__(
        self,
        data: dict,
        event_id: str | None = None,
        response_type: Literal[ResponseType.DATA] | None = None,
        **kwargs,  # pylint: disable=unused-argument
    ):
        event_id = event_id or str(uuid4())

        super().__init__(response_type=ResponseType.DATA, event_id=event_id, data=data, **kwargs)

    response_type: Literal[ResponseType.DATA]
    event_id: str = Field(..., description="")
    data: dict = Field(..., description="Data that should be returned.")


class ErrorResponse(BaseModel):
    def __init__(
        self,
        message: str,
        error_type: str,
        trace: str = "",
        event_id: str | None = None,
        response_type: Literal[ResponseType.ERROR] | None = None,  # pylint: disable=unused-argument
        **kwargs,
    ):
        event_id = event_id or str(uuid4())
        super().__init__(
            response_type=ResponseType.ERROR,
            event_id=event_id,
            message=message,
            error_type=error_type,
            trace=trace,
            **kwargs,
        )

    response_type: Literal[ResponseType.ERROR]
    event_id: str = Field(..., description="")
    message: str = Field(..., description="error message")
    error_type: str = Field(..., description="type of error (e.g. ValueError)")
    trace: str = Field(..., description="trace to the error")


ResponseUnion = Union[WorkloadResponse, DataResponse, ErrorResponse]
Response = Annotated[ResponseUnion, Field(discriminator="response_type")]

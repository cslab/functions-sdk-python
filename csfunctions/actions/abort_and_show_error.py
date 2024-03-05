from typing import Literal

from pydantic import BaseModel, Field

from .base import ActionNames, BaseAction


class AbortAndShowErrorData(BaseModel):
    def __init__(self, message: str, **kwargs):
        super().__init__(message=message, **kwargs)

    message: str = Field("unknown error", description="error message to be shown to the user")


class AbortAndShowErrorAction(BaseAction):
    def __init__(self, id: str, message: str | None = None, **kwargs):  # pylint: disable=redefined-builtin
        if message:
            super().__init__(name=ActionNames.ABORT_AND_SHOW_ERROR, id=id, data=AbortAndShowErrorData(message=message))
        else:
            super().__init__(name=ActionNames.ABORT_AND_SHOW_ERROR, id=id, data=kwargs["data"])

    name: Literal[ActionNames.ABORT_AND_SHOW_ERROR]
    data: AbortAndShowErrorData

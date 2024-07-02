from typing import Literal

from pydantic import Field

from .base import ActionNames, BaseAction


class AbortAndShowErrorAction(BaseAction):
    name: Literal[ActionNames.ABORT_AND_SHOW_ERROR] = ActionNames.ABORT_AND_SHOW_ERROR
    message: str = Field("unknown error", description="error message to be shown to the user")

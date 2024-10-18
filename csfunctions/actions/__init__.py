from typing import Annotated, Union

from pydantic import Field

from .abort_and_show_error import AbortAndShowErrorAction
from .base import ActionNames
from .dummy import DummyAction

ActionUnion = Union[AbortAndShowErrorAction, DummyAction]
Action = Annotated[ActionUnion, Field(discriminator="name")]

__all__ = [
    "Action",
    "ActionNames",
    "DummyAction",
    "AbortAndShowErrorAction",
    "ActionUnion",
]

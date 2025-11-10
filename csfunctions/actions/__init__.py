from typing import Annotated

from pydantic import Field

from .abort_and_show_error import AbortAndShowErrorAction
from .base import ActionNames
from .dummy import DummyAction
from .start_workflow import StartWorkflowAction

ActionUnion = AbortAndShowErrorAction | DummyAction | StartWorkflowAction
Action = Annotated[ActionUnion, Field(discriminator="name")]

__all__ = [
    "Action",
    "ActionNames",
    "DummyAction",
    "AbortAndShowErrorAction",
    "ActionUnion",
    "StartWorkflowAction",
]

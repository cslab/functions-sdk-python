from typing import Literal

from .base import ActionNames, BaseAction


class DummyAction(BaseAction):
    """
    Dummy Action, for unit testing
    """

    name: Literal[ActionNames.DUMMY] = ActionNames.DUMMY

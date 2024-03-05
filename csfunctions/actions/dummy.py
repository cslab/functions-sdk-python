from typing import Literal

from .base import ActionNames, BaseAction


class DummyAction(BaseAction):
    """
    Dummy Action, for unit testing
    """

    def __init__(self, id: str, **kwargs):  # pylint: disable=redefined-builtin
        super().__init__(name=ActionNames.DUMMY, id=id, data=kwargs["data"])

    name: Literal[ActionNames.DUMMY]

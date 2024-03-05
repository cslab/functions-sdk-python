from typing import Annotated, Union

from pydantic import Field

from .abort_and_show_error import AbortAndShowErrorAction
from .dummy import DummyAction

Action = Annotated[Union[AbortAndShowErrorAction, DummyAction], Field(discriminator="name")]

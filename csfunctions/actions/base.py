from enum import Enum

from pydantic import BaseModel


class ActionNames(str, Enum):
    ABORT_AND_SHOW_ERROR = "abort_and_show_error"
    DOWNLOAD_FILE = "download_file"
    DUMMY = "dummy"
    START_WORKFLOW = "start_workflow"


class BaseAction(BaseModel):
    name: str
    id: str | None = None

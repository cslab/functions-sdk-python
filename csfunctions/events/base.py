from enum import Enum

from pydantic import BaseModel, Field


class EventNames(str, Enum):
    DUMMY = "dummy"
    DOCUMENT_RELEASE = "document_release"
    DOCUMENT_RELEASE_CHECK = "document_release_check"
    PART_RELEASE = "part_release"
    PART_RELEASE_CHECK = "part_release_check"
    ENGINEERING_CHANGE_RELEASE = "engineering_change_release"
    ENGINEERING_CHANGE_RELEASE_CHECK = "engineering_change_release_check"
    FIELD_VALUE_CALCULATION = "field_value_calculation"
    WORKFLOW_TASK_TRIGGER = "workflow_task_trigger"


class BaseEvent(BaseModel):
    name: str
    event_id: str = Field(..., description="unique identifier")

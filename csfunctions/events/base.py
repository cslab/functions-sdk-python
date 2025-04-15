from enum import Enum

from pydantic import BaseModel, Field


class EventNames(str, Enum):
    DUMMY = "dummy"
    DOCUMENT_RELEASED = "document_released"
    DOCUMENT_RELEASE_CHECK = "document_release_check"
    DOCUMENT_FIELD_CALCULATION = "document_field_calculation"
    PART_RELEASED = "part_released"
    PART_RELEASE_CHECK = "part_release_check"
    PART_FIELD_CALCULATION = "part_field_calculation"
    ENGINEERING_CHANGE_RELEASED = "engineering_change_released"
    ENGINEERING_CHANGE_RELEASE_CHECK = "engineering_change_release_check"
    FIELD_VALUE_CALCULATION = "field_value_calculation"
    WORKFLOW_TASK_TRIGGER = "workflow_task_trigger"
    DOCUMENT_CREATE_CHECK = "document_create_check"
    DOCUMENT_MODIFY_CHECK = "document_modify_check"
    PART_CREATE_CHECK = "part_create_check"
    PART_MODIFY_CHECK = "part_modify_check"
    ENGINEERING_CHANGE_STATUS_CHANGED = "engineering_change_status_changed"
    ENGINEERING_CHANGE_STATUS_CHANGE_CHECK = "engineering_change_status_change_check"


class BaseEvent(BaseModel):
    name: str
    event_id: str = Field(..., description="unique identifier")

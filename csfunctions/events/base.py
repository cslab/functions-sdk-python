from enum import Enum

from pydantic import BaseModel, Field


class EventNames(str, Enum):
    DUMMY = "dummy"
    DOCUMENT_CREATED = "document_created"
    DOCUMENT_RELEASED = "document_released"
    DOCUMENT_RELEASE_CHECK = "document_release_check"
    DOCUMENT_FIELD_CALCULATION = "document_field_calculation"
    PART_CREATED = "part_created"
    PART_RELEASED = "part_released"
    PART_RELEASE_CHECK = "part_release_check"
    PART_FIELD_CALCULATION = "part_field_calculation"
    BOM_ITEM_FIELD_CALCULATION = "bom_item_field_calculation"
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
    CHANGE_ORDER_RELEASED = "change_order_released"
    CHANGE_ORDER_RELEASE_CHECK = "change_order_release_check"
    CHANGE_ORDER_STATUS_CHANGED = "change_order_status_changed"
    CHANGE_ORDER_STATUS_CHANGE_CHECK = "change_order_status_change_check"
    CHANGE_REQUEST_RELEASED = "change_request_released"
    CHANGE_REQUEST_RELEASE_CHECK = "change_request_release_check"
    CHANGE_REQUEST_STATUS_CHANGED = "change_request_status_changed"
    CHANGE_REQUEST_STATUS_CHANGE_CHECK = "change_request_status_change_check"
    CUSTOM_OPERATION_DOCUMENT = "custom_operation_document"
    CUSTOM_OPERATION_PART = "custom_operation_part"


class BaseEvent(BaseModel):
    name: str
    event_id: str = Field(..., description="unique identifier")

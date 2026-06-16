from typing import Annotated

from pydantic import Field

from .bom_item_field_calculation import BOMItemFieldCalculationData, BOMItemFieldCalculationEvent
from .change_order_release_check import ChangeOrderReleaseCheckData, ChangeOrderReleaseCheckEvent
from .change_order_released import ChangeOrderReleasedData, ChangeOrderReleasedEvent
from .change_order_status_change_check import ChangeOrderStatusChangeCheckData, ChangeOrderStatusChangeCheckEvent
from .change_order_status_changed import ChangeOrderStatusChangedData, ChangeOrderStatusChangedEvent
from .change_request_release_check import ChangeRequestReleaseCheckData, ChangeRequestReleaseCheckEvent
from .change_request_released import ChangeRequestReleasedData, ChangeRequestReleasedEvent
from .change_request_status_change_check import ChangeRequestStatusChangeCheckData, ChangeRequestStatusChangeCheckEvent
from .change_request_status_changed import ChangeRequestStatusChangedData, ChangeRequestStatusChangedEvent
from .custom_operations import (
    CustomOperationDocumentData,
    CustomOperationDocumentEvent,
    CustomOperationPartData,
    CustomOperationPartEvent,
)
from .dialog_data import DocumentReleasedDialogData, PartReleasedDialogData
from .document_create_check import DocumentCreateCheckData, DocumentCreateCheckEvent
from .document_field_calculation import DocumentFieldCalculationData, DocumentFieldCalculationEvent
from .document_modify_check import DocumentModifyCheckData, DocumentModifyCheckEvent
from .document_release_check import DocumentReleaseCheckData, DocumentReleaseCheckEvent
from .document_released import DocumentReleasedData, DocumentReleasedEvent
from .dummy import DummyEvent, DummyEventData
from .engineering_change_release_check import EngineeringChangeReleaseCheckData, EngineeringChangeReleaseCheckEvent
from .engineering_change_released import EngineeringChangeReleasedData, EngineeringChangeReleasedEvent
from .engineering_change_status_change_check import (
    EngineeringChangeStatusChangeCheckData,
    EngineeringChangeStatusChangeCheckEvent,
)
from .engineering_change_status_changed import EngineeringChangeStatusChangedData, EngineeringChangeStatusChangedEvent
from .field_value_calculation import FieldValueCalculationData, FieldValueCalculationEvent
from .part_create_check import PartCreateCheckData, PartCreateCheckEvent
from .part_field_calculation import PartFieldCalculationData, PartFieldCalculationEvent
from .part_modify_check import PartModifyCheckData, PartModifyCheckEvent
from .part_release_check import PartReleaseCheckData, PartReleaseCheckEvent
from .part_released import PartReleasedData, PartReleasedEvent
from .workflow_task_trigger import WorkflowTaskTriggerEvent, WorkflowTaskTriggerEventData

Event = Annotated[
    DocumentReleasedEvent
    | DocumentReleaseCheckEvent
    | DocumentFieldCalculationEvent
    | PartReleasedEvent
    | PartReleaseCheckEvent
    | PartFieldCalculationEvent
    | BOMItemFieldCalculationEvent
    | FieldValueCalculationEvent
    | DummyEvent
    | EngineeringChangeReleasedEvent
    | EngineeringChangeReleaseCheckEvent
    | EngineeringChangeStatusChangedEvent
    | EngineeringChangeStatusChangeCheckEvent
    | ChangeOrderReleasedEvent
    | ChangeOrderReleaseCheckEvent
    | ChangeOrderStatusChangedEvent
    | ChangeOrderStatusChangeCheckEvent
    | ChangeRequestReleasedEvent
    | ChangeRequestReleaseCheckEvent
    | ChangeRequestStatusChangedEvent
    | ChangeRequestStatusChangeCheckEvent
    | WorkflowTaskTriggerEvent
    | DocumentCreateCheckEvent
    | DocumentModifyCheckEvent
    | PartCreateCheckEvent
    | PartModifyCheckEvent
    | CustomOperationDocumentEvent
    | CustomOperationPartEvent,
    Field(discriminator="name"),
]
EventData = (
    DocumentReleasedData
    | DocumentReleaseCheckData
    | DocumentFieldCalculationData
    | PartReleasedData
    | PartReleaseCheckData
    | PartFieldCalculationData
    | BOMItemFieldCalculationData
    | FieldValueCalculationData
    | DummyEventData
    | EngineeringChangeReleasedData
    | EngineeringChangeReleaseCheckData
    | EngineeringChangeStatusChangedData
    | EngineeringChangeStatusChangeCheckData
    | ChangeOrderReleasedData
    | ChangeOrderReleaseCheckData
    | ChangeOrderStatusChangedData
    | ChangeOrderStatusChangeCheckData
    | ChangeRequestReleasedData
    | ChangeRequestReleaseCheckData
    | ChangeRequestStatusChangedData
    | ChangeRequestStatusChangeCheckData
    | WorkflowTaskTriggerEventData
    | DocumentCreateCheckData
    | DocumentModifyCheckData
    | PartCreateCheckData
    | PartModifyCheckData
    | CustomOperationDocumentData
    | CustomOperationPartData
)

__all__ = [
    "DocumentReleasedEvent",
    "DocumentReleaseCheckEvent",
    "DocumentFieldCalculationEvent",
    "PartReleasedEvent",
    "PartReleaseCheckEvent",
    "PartFieldCalculationEvent",
    "BOMItemFieldCalculationEvent",
    "FieldValueCalculationEvent",
    "DummyEvent",
    "EngineeringChangeReleasedEvent",
    "EngineeringChangeReleaseCheckEvent",
    "EngineeringChangeStatusChangedEvent",
    "EngineeringChangeStatusChangeCheckEvent",
    "ChangeOrderReleasedEvent",
    "ChangeOrderReleaseCheckEvent",
    "ChangeOrderStatusChangedEvent",
    "ChangeOrderStatusChangeCheckEvent",
    "ChangeRequestReleasedEvent",
    "ChangeRequestReleaseCheckEvent",
    "ChangeRequestStatusChangedEvent",
    "ChangeRequestStatusChangeCheckEvent",
    "WorkflowTaskTriggerEvent",
    "DocumentReleasedData",
    "DocumentReleaseCheckData",
    "DocumentFieldCalculationData",
    "PartReleasedData",
    "PartReleaseCheckData",
    "BOMItemFieldCalculationData",
    "FieldValueCalculationData",
    "DummyEventData",
    "EngineeringChangeReleasedData",
    "EngineeringChangeReleaseCheckData",
    "EngineeringChangeStatusChangedData",
    "EngineeringChangeStatusChangeCheckData",
    "ChangeOrderReleasedData",
    "ChangeOrderReleaseCheckData",
    "ChangeOrderStatusChangedData",
    "ChangeOrderStatusChangeCheckData",
    "ChangeRequestReleasedData",
    "ChangeRequestReleaseCheckData",
    "ChangeRequestStatusChangedData",
    "ChangeRequestStatusChangeCheckData",
    "WorkflowTaskTriggerEventData",
    "DocumentReleasedDialogData",
    "PartReleasedDialogData",
    "PartFieldCalculationData",
    "DocumentCreateCheckData",
    "DocumentCreateCheckEvent",
    "DocumentModifyCheckData",
    "DocumentModifyCheckEvent",
    "PartCreateCheckData",
    "PartCreateCheckEvent",
    "PartModifyCheckData",
    "PartModifyCheckEvent",
    "CustomOperationDocumentData",
    "CustomOperationDocumentEvent",
    "CustomOperationPartData",
    "CustomOperationPartEvent",
]

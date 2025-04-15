from typing import Annotated, Union

from pydantic import Field

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
    Union[
        DocumentReleasedEvent,
        DocumentReleaseCheckEvent,
        DocumentFieldCalculationEvent,
        PartReleasedEvent,
        PartReleaseCheckEvent,
        PartFieldCalculationEvent,
        FieldValueCalculationEvent,
        DummyEvent,
        EngineeringChangeReleasedEvent,
        EngineeringChangeReleaseCheckEvent,
        EngineeringChangeStatusChangedEvent,
        EngineeringChangeStatusChangeCheckEvent,
        WorkflowTaskTriggerEvent,
        DocumentCreateCheckEvent,
        DocumentModifyCheckEvent,
        PartCreateCheckEvent,
        PartModifyCheckEvent,
    ],
    Field(discriminator="name"),
]
EventData = Union[
    DocumentReleasedData,
    DocumentReleaseCheckData,
    DocumentFieldCalculationData,
    PartReleasedData,
    PartReleaseCheckData,
    PartFieldCalculationData,
    FieldValueCalculationData,
    DummyEventData,
    EngineeringChangeReleasedData,
    EngineeringChangeReleaseCheckData,
    EngineeringChangeStatusChangedData,
    EngineeringChangeStatusChangeCheckData,
    WorkflowTaskTriggerEventData,
    DocumentCreateCheckData,
    DocumentModifyCheckData,
    PartCreateCheckData,
    PartModifyCheckData,
]

__all__ = [
    "DocumentReleasedEvent",
    "DocumentReleaseCheckEvent",
    "DocumentFieldCalculationEvent",
    "PartReleasedEvent",
    "PartReleaseCheckEvent",
    "PartFieldCalculationEvent",
    "FieldValueCalculationEvent",
    "DummyEvent",
    "EngineeringChangeReleasedEvent",
    "EngineeringChangeReleaseCheckEvent",
    "WorkflowTaskTriggerEvent",
    "DocumentReleasedData",
    "DocumentReleaseCheckData",
    "DocumentFieldCalculationData",
    "PartReleasedData",
    "PartReleaseCheckData",
    "FieldValueCalculationData",
    "DummyEventData",
    "EngineeringChangeReleasedData",
    "EngineeringChangeReleaseCheckData",
    "EngineeringChangeStatusChangedData",
    "EngineeringChangeStatusChangeCheckData",
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
]

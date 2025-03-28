from typing import Annotated, Union

from pydantic import Field

from .dialog_data import DocumentReleaseDialogData, PartReleaseDialogData
from .document_create_check import DocumentCreateCheckData, DocumentCreateCheckEvent
from .document_field_calculation import DocumentFieldCalculationData, DocumentFieldCalculationEvent
from .document_modify_check import DocumentModifyCheckData, DocumentModifyCheckEvent
from .document_release import DocumentReleaseData, DocumentReleaseEvent
from .document_release_check import DocumentReleaseCheckData, DocumentReleaseCheckEvent
from .dummy import DummyEvent, DummyEventData
from .engineering_change_release import EngineeringChangeRelease, EngineeringChangeReleaseData
from .engineering_change_release_check import EngineeringChangeReleaseCheck, EngineeringChangeReleaseCheckData
from .field_value_calculation import FieldValueCalculationData, FieldValueCalculationEvent
from .part_create_check import PartCreateCheckData, PartCreateCheckEvent
from .part_field_calculation import PartFieldCalculationData, PartFieldCalculationEvent
from .part_modify_check import PartModifyCheckData, PartModifyCheckEvent
from .part_release import PartReleaseData, PartReleaseEvent
from .part_release_check import PartReleaseCheckData, PartReleaseCheckEvent
from .workflow_task_trigger import WorkflowTaskTriggerEvent, WorkflowTaskTriggerEventData

Event = Annotated[
    Union[
        DocumentReleaseEvent,
        DocumentReleaseCheckEvent,
        DocumentFieldCalculationEvent,
        PartReleaseEvent,
        PartReleaseCheckEvent,
        PartFieldCalculationEvent,
        FieldValueCalculationEvent,
        DummyEvent,
        EngineeringChangeRelease,
        EngineeringChangeReleaseCheck,
        WorkflowTaskTriggerEvent,
        DocumentCreateCheckEvent,
        DocumentModifyCheckEvent,
        PartCreateCheckEvent,
        PartModifyCheckEvent,
    ],
    Field(discriminator="name"),
]
EventData = Union[
    DocumentReleaseData,
    DocumentReleaseCheckData,
    DocumentFieldCalculationData,
    PartReleaseData,
    PartReleaseCheckData,
    PartFieldCalculationData,
    FieldValueCalculationData,
    DummyEventData,
    EngineeringChangeReleaseData,
    EngineeringChangeReleaseCheckData,
    WorkflowTaskTriggerEventData,
    DocumentCreateCheckData,
    DocumentModifyCheckData,
    PartCreateCheckData,
    PartModifyCheckData,
]

__all__ = [
    "DocumentReleaseEvent",
    "DocumentReleaseCheckEvent",
    "DocumentFieldCalculationEvent",
    "PartReleaseEvent",
    "PartReleaseCheckEvent",
    "PartFieldCalculationEvent",
    "FieldValueCalculationEvent",
    "DummyEvent",
    "EngineeringChangeRelease",
    "EngineeringChangeReleaseCheck",
    "WorkflowTaskTriggerEvent",
    "DocumentReleaseData",
    "DocumentReleaseCheckData",
    "DocumentFieldCalculationData",
    "PartReleaseData",
    "PartReleaseCheckData",
    "FieldValueCalculationData",
    "DummyEventData",
    "EngineeringChangeReleaseData",
    "EngineeringChangeReleaseCheckData",
    "WorkflowTaskTriggerEventData",
    "DocumentReleaseDialogData",
    "PartReleaseDialogData",
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

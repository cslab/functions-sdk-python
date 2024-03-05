from typing import Annotated, Union

from pydantic import Field

from .document_release import DocumentReleaseData, DocumentReleaseDialogData, DocumentReleaseEvent
from .dummy import DummyEvent, DummyEventData
from .engineering_change_release import EngineeringChangeRelease, EngineeringChangeReleaseData
from .field_value_calculation import FieldValueCalculationData, FieldValueCalculationEvent
from .part_release import PartReleaseData, PartReleaseDialogData, PartReleaseEvent
from .workflow_task_trigger import WorkflowTaskTriggerEvent, WorkflowTaskTriggerEventData

Event = Annotated[
    Union[
        DocumentReleaseEvent,
        PartReleaseEvent,
        FieldValueCalculationEvent,
        DummyEvent,
        EngineeringChangeRelease,
        WorkflowTaskTriggerEvent,
    ],
    Field(discriminator="name"),
]
EventData = Union[
    DocumentReleaseData,
    PartReleaseData,
    FieldValueCalculationData,
    DummyEventData,
    EngineeringChangeReleaseData,
    WorkflowTaskTriggerEventData,
]

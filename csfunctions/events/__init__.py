from typing import Annotated, Union

from pydantic import Field

from .dialog_data import DocumentReleaseDialogData, PartReleaseDialogData
from .document_release import DocumentReleaseData, DocumentReleaseEvent
from .dummy import DummyEvent, DummyEventData
from .engineering_change_release import EngineeringChangeRelease, EngineeringChangeReleaseData
from .field_value_calculation import FieldValueCalculationData, FieldValueCalculationEvent
from .part_release import PartReleaseData, PartReleaseEvent
from .release_check import ReleaseCheckData, ReleaseCheckEvent
from .released import ReleasedData, ReleasedEvent
from .workflow_task_trigger import WorkflowTaskTriggerEvent, WorkflowTaskTriggerEventData

Event = Annotated[
    Union[
        DocumentReleaseEvent,
        PartReleaseEvent,
        FieldValueCalculationEvent,
        DummyEvent,
        EngineeringChangeRelease,
        WorkflowTaskTriggerEvent,
        ReleaseCheckEvent,
        ReleasedEvent,
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
    ReleaseCheckData,
    ReleasedData,
]

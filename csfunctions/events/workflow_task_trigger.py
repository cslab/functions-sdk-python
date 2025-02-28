from typing import Literal

from pydantic import BaseModel, Field

from csfunctions.objects import Briefcase, Document, EngineeringChange, Part, Workflow

from .base import BaseEvent, EventNames


class WorkflowTaskTriggerEventData(BaseModel):
    workflows: list[Workflow] = Field(..., description="List of workflows in this event")
    parts: list[Part] = Field([], description="List if parts attached to the workflow.")
    documents: list[Document] = Field([], description="List if documents attached to the workflow.")
    engineering_changes: list[EngineeringChange] = Field(
        [], description="List of engineering changes attached to the workflow."
    )
    briefcases: list[Briefcase] = Field([], description="List of briefcases attached to the workflow.")


class WorkflowTaskTriggerEvent(BaseEvent):
    name: Literal[EventNames.WORKFLOW_TASK_TRIGGER] = EventNames.WORKFLOW_TASK_TRIGGER
    data: WorkflowTaskTriggerEventData

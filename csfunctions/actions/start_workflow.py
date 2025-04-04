from typing import Literal

from pydantic import BaseModel, Field

from .base import ActionNames, BaseAction


class TaskParameter(BaseModel):
    task_id: str = Field(..., description="Identifier for the task this parameter belongs to")
    name: str = Field(..., description="Name of the parameter")
    value: str = Field(..., description="Value of the parameter")


class StartWorkflowAction(BaseAction):
    name: Literal[ActionNames.START_WORKFLOW] = ActionNames.START_WORKFLOW
    template_id: str = Field(..., description="ID of the workflow template to start")
    cdb_project_id: str | None = Field(
        default=None, description="ID of the project in which the workflow should be started"
    )
    title: str = Field(..., description="Title of the workflow")
    attachment_ids: list[str] = Field(
        default_factory=list, description="List of cdb_object_ids to attach to the workflow"
    )
    global_briefcase_object_ids: list[str] = Field(
        default_factory=list, description="List of cdb_object_ids to attach to the global briefcase"
    )
    task_parameters: list[TaskParameter] = Field(default_factory=list, description="List of task parameters")

from typing import Literal, Optional

from pydantic import BaseModel, Field

from .base import ActionNames, BaseAction


class Subject(BaseModel):
    subject_id: str = Field(..., description="ID of the subject, eg. a role name or personalnummer")
    subject_type: Literal["Person", "PCS Role", "Common Role"] = Field(
        ..., description="Type of the subject: Person, PCS Role or Common Role"
    )


class TaskConfiguration(BaseModel):
    task_id: str = Field(..., description="Identifier for the task")
    responsible: Optional[Subject] = Field(default=None, description="Responsible subject for the task")
    recipients: list[Subject] = Field(
        default_factory=list,
        description="List of recipients for the task (only used by information tasks)",
    )
    description: str | None = Field(
        default=None,
        description="Description of the task. If not set, the existing description will be kept. "
        "(max. 1024 characters)",
        max_length=1024,
    )
    title: str | None = Field(
        default=None,
        description="Title of the task. If not set, the existing title will be kept. (max. 60 characters)",
        max_length=60,
    )


class StartWorkflowAction(BaseAction):
    name: Literal[ActionNames.START_WORKFLOW] = ActionNames.START_WORKFLOW
    template_id: str = Field(..., description="ID of the workflow template to start")
    cdb_project_id: str | None = Field(
        default=None,
        description="ID of the project in which the workflow should be started",
    )
    title: str = Field(..., description="Title of the workflow (max. 255 characters)", max_length=255)
    attachment_ids: list[str] = Field(
        default_factory=list,
        description="List of cdb_object_ids to attach to the workflow",
    )
    global_briefcase_object_ids: list[str] = Field(
        default_factory=list,
        description="List of cdb_object_ids to attach to the global briefcase",
    )
    task_configurations: list[TaskConfiguration] = Field(
        default_factory=list, description="List of task configurations"
    )

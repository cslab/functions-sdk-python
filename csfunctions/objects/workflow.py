from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import Field

from .base import BaseObject, ObjectType
from .briefcase import Briefcase

if TYPE_CHECKING:
    from csfunctions.events import EventData


class Workflow(BaseObject):
    object_type: Literal[ObjectType.WORKFLOW] = ObjectType.WORKFLOW

    cdb_process_id: str = Field(..., description="Workflow ID")
    title: str | None = Field("", description="Title")
    started_at: datetime | None = Field(None, description="Date when the workflow was started.")
    started_by: str | None = Field(None, description="ID of the user who started the workflow.")

    local_briefcase_ids: list[str] = Field([], description="List of local briefcase ids (cdb_object_id)")
    global_briefcase_ids: list[str] = Field([], description="List of global briefcase ids (cdb_object_id)")

    local_briefcases: list[Briefcase] = Field([], exclude=True)
    global_briefcases: list[Briefcase] = Field([], exclude=True)

    def link_objects(self, data: "EventData"):
        local_briefcases: list[Briefcase] | None = getattr(data, "local_briefcases", None)
        global_briefcases: list[Briefcase] | None = getattr(data, "local_briefcases", None)

        if local_briefcases and self.local_briefcase_ids:
            self._link_local_briefcases(local_briefcases)

        if global_briefcases and self.global_briefcase_ids:
            self._link_global_briefcases(global_briefcases)

    def _link_local_briefcases(self, local_briefcases: list["Briefcase"]):
        for local_briefcase in local_briefcases:
            if (
                local_briefcase.cdb_object_id in self.local_briefcase_ids
                and local_briefcase not in self.local_briefcases
            ):
                self.local_briefcases.append(local_briefcase)

    def _link_global_briefcases(self, global_briefcases: list["Briefcase"]):
        for global_briefcase in global_briefcases:
            if (
                global_briefcase.cdb_object_id in self.global_briefcase_ids
                and global_briefcase not in self.global_briefcases
            ):
                self.global_briefcases.append(global_briefcase)

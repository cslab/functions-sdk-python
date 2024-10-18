from typing import TYPE_CHECKING, Literal

from pydantic import Field

from .base import BaseObject, ObjectType
from .document import Document
from .engineering_change import EngineeringChange
from .part import Part

if TYPE_CHECKING:
    from csfunctions.events import EventData


class Briefcase(BaseObject):
    """
    Briefcases are used by Workflows and can contain parts, documents or engineering changes.
    """

    object_type: Literal[ObjectType.BRIEFCASE] = ObjectType.BRIEFCASE

    cdb_object_id: str = Field(..., description="Briefcase ID")
    name: str | None = Field("", description="Briefcase Name")
    part_ids: list[str] = Field([], description="List of part IDs in this Briefcase. (teilenummer@t_index)")
    document_ids: list[str] = Field([], description="List of document IDs in this Briefcase. (z_nummer@z_index)")
    engineering_change_ids: list[str] = Field(
        [], description="List of engineering change IDs in this Briefcase. (cdb_ec_id)"
    )

    parts: list[Part] = Field([], exclude=True)
    documents: list[Document] = Field([], exclude=True)
    engineering_changes: list[EngineeringChange] = Field([], exclude=True)

    def link_objects(self, data: "EventData"):
        parts = getattr(data, "parts", None)
        documents = getattr(data, "documents", None)
        engineering_changes = getattr(data, "engineering_changes", None)

        if parts and self.part_ids:
            self._link_parts(parts)
        if documents and self.document_ids:
            self._link_documents(documents)
        if engineering_changes and self.engineering_change_ids:
            self._link_engineering_changes(engineering_changes)

    def _link_parts(self, parts: list["Part"]):
        for part in parts:
            if f"{part.teilenummer}@{part.t_index}" in self.part_ids and part not in self.parts:
                self.parts.append(part)

    def _link_documents(self, documents: list["Document"]):
        for document in documents:
            if f"{document.z_nummer}@{document.z_index}" in self.document_ids and document not in self.documents:
                self.documents.append(document)

    def _link_engineering_changes(self, engineering_changes: list["EngineeringChange"]):
        for engineering_change in engineering_changes:
            if (
                engineering_change.cdb_ec_id in self.engineering_change_ids
                and engineering_change not in self.engineering_changes
            ):
                self.engineering_changes.append(engineering_change)

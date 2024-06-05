from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import Field

from .base import BaseObject, ObjectType
from .document import Document
from .part import Part

if TYPE_CHECKING:
    from csfunctions.events import EventData


class EngineeringChange(BaseObject):
    object_type: Literal[ObjectType.ENGINEERING_CHANGE] = ObjectType.ENGINEERING_CHANGE

    cdb_ec_id: str = Field(..., description="Engineering Change ID")
    cdb_project_id: str | None = Field("", description="Project ID")
    ec_state: str = Field("", description="")
    end_time_plan: datetime | None = Field(None, description="Planned end time")
    status: int = Field(..., description="Status")
    title: str | None = Field("", description="Title")
    template_ec_id: str | None = Field("", description="Template ID")
    cdb_object_id: str | None = Field(None, description="Object ID")

    c_department: str | None = Field("", description="Department")
    c_description: str | None = Field("", description="Description")
    c_event: str | None = Field("", description="Event")
    c_reason: str | None = Field("", description="Reason")
    c_source: str | None = Field("", description="Source")
    category: str | None = Field("", description="Category")

    part_ids: list[str] = Field([], description="List of part IDs, that were changed. (teilenummer@t_index)")
    document_ids: list[str] = Field([], description="List of document IDs, that were changed. (z_nummer@z_index)")

    planned_changes_part_ids: list[str] = Field(
        [], description="List of part IDs, that were planned to be changed. (teilenummer@t_index)"
    )
    planned_changes_document_ids: list[str] = Field(
        [], description="List of document IDs, that were planned to be changed. (z_nummer@z_index)"
    )
    accompanying_document_ids: list[str] = Field(
        [], description="List of document IDs, that accompany the change. (z_nummer@z_index)"
    )

    parts: list[Part] = Field([], exclude=True)
    documents: list[Document] = Field([], exclude=True)

    planned_changes_parts: list[Part] = Field([], exclude=True)
    planned_changes_documents: list[Document] = Field([], exclude=True)

    accompanying_documents: list[Document] = Field([], exclude=True)

    cdb_cpersno: str | None = Field("", description="Created by")
    cdb_cdate: datetime | None = Field(None, description="Created on")
    cdb_mpersno: str = Field("", description="Last Modified by")
    cdb_mdate: datetime | None = Field(None, description="Last Modified on")

    def link_objects(self, data: "EventData"):
        parts = getattr(data, "parts", None)
        documents = getattr(data, "documents", None)

        if parts and self.part_ids:
            self._link_parts(parts)
        if parts and self.planned_changes_part_ids:
            self._link_planned_changes_parts(parts)

        if documents and self.document_ids:
            self._link_documents(documents)
        if documents and self.planned_changes_document_ids:
            self._link__planned_changes_documents(documents)
        if documents and self.accompanying_document_ids:
            self._link_accompanying_documents(documents)

    def _link_parts(self, parts: list["Part"]):
        for part in parts:
            if f"{part.teilenummer}@{part.t_index}" in self.part_ids and part not in self.parts:
                self.parts.append(part)

    def _link_documents(self, documents: list["Document"]):
        for document in documents:
            if f"{document.z_nummer}@{document.z_index}" in self.document_ids and document not in self.documents:
                self.documents.append(document)

    def _link_planned_changes_parts(self, planned_changes_parts: list["Part"]):
        for part in planned_changes_parts:
            if (
                f"{part.teilenummer}@{part.t_index}" in self.planned_changes_part_ids
                and part not in self.planned_changes_parts
            ):
                self.planned_changes_parts.append(part)

    def _link__planned_changes_documents(self, planned_changes_documents: list["Document"]):
        for document in planned_changes_documents:
            if (
                f"{document.z_nummer}@{document.z_index}" in self.planned_changes_document_ids
                and document not in self.planned_changes_documents
            ):
                self.planned_changes_documents.append(document)

    def _link_accompanying_documents(self, accompanying_documents: list["Document"]):
        for document in accompanying_documents:
            if (
                f"{document.z_nummer}@{document.z_index}" in self.accompanying_document_ids
                and document not in self.accompanying_documents
            ):
                self.accompanying_documents.append(document)

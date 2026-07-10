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


class Change(BaseObject):
    """
    Base class for changes of the ECM module (change orders and change requests).
    Use the concrete subclasses :class:`ChangeOrder` and :class:`ChangeRequest`.
    """

    cs_change_id: str = Field(..., description="Change ID")
    cdb_project_id: str | None = Field("", description="Project ID")
    product_object_oid: str | None = Field("", description="Product object ID")
    end_time_plan: datetime | None = Field(None, description="Planned end time")
    status: int = Field(..., description="Status")
    title_de: str | None = Field("", description="Title (de)")
    title_en: str | None = Field("", description="Title (en)")
    title_ja: str | None = Field("", description="Title (ja)")
    title_zh: str | None = Field("", description="Title (zh)")
    cdb_object_id: str | None = Field(None, description="Object ID")
    change_type: str | None = Field(None, description="Change Type")

    cs_ecm_change_description_de: str | None = Field("", description="Description (de)")
    cs_ecm_change_description_en: str | None = Field("", description="Description (en)")
    cs_ecm_change_description_ja: str | None = Field("", description="Description (ja)")
    cs_ecm_change_description_zh: str | None = Field("", description="Description (zh)")
    c_event: str | None = Field("", description="Event")
    change_reason_de: str | None = Field("", description="Reason (de)")
    change_reason_en: str | None = Field("", description="Reason (en)")
    change_reason_ja: str | None = Field("", description="Reason (ja)")
    change_reason_zh: str | None = Field("", description="Reason (zh)")
    c_source: str | None = Field("", description="Source")

    part_ids: list[str] = Field([], description="List of part IDs, that were changed. (teilenummer@t_index)")
    document_ids: list[str] = Field([], description="List of document IDs, that were changed. (z_nummer@z_index)")

    affected_part_ids: list[str] = Field(
        [], description="List of part IDs, that were planned to be changed. (teilenummer@t_index)"
    )
    affected_document_ids: list[str] = Field(
        [], description="List of document IDs, that were planned to be changed. (z_nummer@z_index)"
    )
    accompanying_document_ids: list[str] = Field(
        [], description="List of document IDs, that accompany the change. (z_nummer@z_index)"
    )

    parts: list[Part] = Field([], exclude=True)
    documents: list[Document] = Field([], exclude=True)

    affected_parts: list[Part] = Field([], exclude=True)
    affected_documents: list[Document] = Field([], exclude=True)

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
        if parts and self.affected_part_ids:
            self._link_affected_parts(parts)

        if documents and self.document_ids:
            self._link_documents(documents)
        if documents and self.affected_document_ids:
            self._link_affected_documents(documents)
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

    def _link_affected_parts(self, affected_parts: list["Part"]):
        for part in affected_parts:
            if f"{part.teilenummer}@{part.t_index}" in self.affected_part_ids and part not in self.affected_parts:
                self.affected_parts.append(part)

    def _link_affected_documents(self, affected_documents: list["Document"]):
        for document in affected_documents:
            if (
                f"{document.z_nummer}@{document.z_index}" in self.affected_document_ids
                and document not in self.affected_documents
            ):
                self.affected_documents.append(document)

    def _link_accompanying_documents(self, accompanying_documents: list["Document"]):
        for document in accompanying_documents:
            if (
                f"{document.z_nummer}@{document.z_index}" in self.accompanying_document_ids
                and document not in self.accompanying_documents
            ):
                self.accompanying_documents.append(document)


class ChangeOrder(Change):
    object_type: Literal[ObjectType.CHANGE_ORDER] = ObjectType.CHANGE_ORDER


class ChangeRequest(Change):
    object_type: Literal[ObjectType.CHANGE_REQUEST] = ObjectType.CHANGE_REQUEST

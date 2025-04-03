from datetime import date, datetime
from typing import TYPE_CHECKING, Literal, Optional

from pydantic import Field

from csfunctions.util import get_items_of_type

from .base import BaseObject, ObjectType
from .file import File
from .part import Part

if TYPE_CHECKING:
    from csfunctions.events import EventData


class Document(BaseObject):
    """
    Normal Document that doesn't contain a CAD-Model.
    """

    object_type: Literal[ObjectType.DOCUMENT] = ObjectType.DOCUMENT

    z_nummer: str = Field(..., description="document number")
    z_index: str = Field(..., description="index")
    titel: str | None = Field(..., description="title")
    category1_name_en: str | None = Field(..., description="Main Category")
    category1_name_de: str | None = Field(..., description="Main Category")
    category2_name_en: str | None = Field(..., description="Category")
    category2_name_de: str | None = Field(..., description="Category")
    z_categ1: str | None = Field(..., description="Main Category")
    z_categ2: str | None = Field(..., description="Category")
    cdb_obsolete: int | None = Field(..., description="Obsolete")
    z_status: int = Field(..., description="Status Number")
    z_status_txt: str = Field(..., description="Status Text")
    autoren: str | None = Field(..., description="Authors, comma separated")
    z_bereich: str | None = Field("", description="Department.")
    z_language: str | None = Field("", description="language")
    keywords: str | None = Field("", description="Keywords")
    z_bemerkung: str | None = Field("", description="Remarks")
    joined_status_name: str | None = Field(..., description="Status")
    erzeug_system: str | None = Field("", description="Program that created the document")
    cdb_lock: str | None = Field("", description="User that locked the document.")
    mapped_cdb_lock_name: str | None = Field(None, description="Username that locked the document.")
    ce_valid_from: date | datetime | None = Field(None, description="Effective from")
    ce_valid_to: date | datetime | None = Field(None, description="Effective to")
    cdb_ec_id: str | None = Field("", description="Engineering Change ID")
    ursprungs_z: str | None = Field("", description="Origin")
    teilenummer: str | None = Field("", description="Part No.")
    t_index: str | None = Field("", description="Part Index")
    cdb_project_id: str | None = Field("", description="Project No.")
    project_name: str | None = Field("", description="Project Name")
    src_name: str | None = Field("", description="Source")
    src_cdate: datetime | None = Field(None, description="Source created on")
    src_rdate: datetime | None = Field(None, description="Source received on")
    src_number: str | None = Field("", description="Original No.")
    src_index: str | None = Field("", description="Original Index")
    src_fname: str | None = Field("", description="Original Filename")
    source_oid: str | None = Field("", description="Based on Template")
    cdb_cpersno: str | None = Field("", description="Created by")
    mapped_cdb_cpersno_name: str | None = Field("", description="Created by")
    cdb_cdate: datetime | None = Field(None, description="Created on")
    cdb_mpersno: str | None = Field("", description="Last Modified by")
    mapped_cdb_mpersno_name: str | None = Field("", description="Last Modified by")
    cdb_mdate: datetime | None = Field(None, description="Last Modified on")
    cdb_m2persno: str | None = Field("", description="File Last Saved by")
    mapped_cdb_m2persno_name: str | None = Field("", description="File Last Saved by")
    cdb_m2date: datetime | None = Field(None, description="File Last Saved on")
    z_art: str | None = Field(None, description="Document Type")
    mapped_materialnr_erp: str | None = Field(None, description="Materialnumber ERP")
    cdb_object_id: str | None = Field(None, description="Object ID")

    files: list[File] = Field([], description="Files attached to the document")

    # in the json schema parts are transferred in parallel to documents, e.g. documents = [...], parts=[...]
    # the execute handler (csfunctions.handler.execute) attaches the parts to the documents that reference them,
    # meaning we need to exclude the part attribute from the json schema
    part: Optional["Part"] = Field(None, exclude=True)

    def link_objects(self, data: "EventData"):
        from .part import Part

        if self.teilenummer:
            parts = get_items_of_type(data, Part)
            self._link_part(parts)

    def _link_part(self, parts: list["Part"]):
        for part in parts:
            if f"{part.teilenummer}@{part.t_index}" == f"{self.teilenummer}@{self.t_index}":
                self.part = part
                return


class CADDocument(Document):
    """
    Special Document type that contains a CAD-Model.
    """

    object_type: Literal[ObjectType.CAD_DOCUMENT] = ObjectType.CAD_DOCUMENT  # type: ignore[assignment]


Part.model_rebuild()

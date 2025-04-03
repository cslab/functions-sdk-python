from datetime import date, datetime
from typing import TYPE_CHECKING, Literal, Optional

from pydantic import Field

from csfunctions.util import get_items_of_type

from .base import BaseObject, ObjectType

if TYPE_CHECKING:
    from csfunctions.events import EventData

    from .document import Document


class Part(BaseObject):
    object_type: Literal[ObjectType.PART] = ObjectType.PART

    teilenummer: str = Field(..., description="part number")
    t_index: str = Field(..., description="part index")
    status: int = Field(..., description="Status Number")
    materialnr_erp: str | None = Field(None, description="Material No. (ERP)")
    benennung: str | None = Field(None, description="Name")
    eng_benennung: str | None = Field(None, description="Name")
    benennung2: str | None = Field(None, description="Additional Name")
    t_kategorie_name_de: str | None = Field(None, description="Category Name")
    t_kategorie_name_en: str | None = Field(None, description="Category Name")
    cdb_t_project_id: str | None = Field(None, description="Project ID")
    t_bereich: str | None = Field(None, description="Department")
    cdb_t_ec_id: str | None = Field(None, description="Engineering Change ID")
    item_maturity: int | None = Field(None, description="Maturity Level")
    gebrauchsstand_name_de: str | None = Field(None, description="Usage Status")
    gebrauchsstand_name_en: str | None = Field(None, description="Usage Status")
    ce_valid_from: date | datetime | None = Field(None, description="Effective from")
    ce_valid_to: date | datetime | None = Field(None, description="Effective to")
    mengeneinheit_name_de: str | None = Field(None, description="Quantity Unit")
    mengeneinheit_name_en: str | None = Field(None, description="Quantity Unit")
    st_gewicht: Optional[float] = Field(None, description="Weight (kg)")
    material_object_id: str | None = Field(None, description="Material ID")
    surface_name_en: str | None = Field(None, description="Surface")
    surface_name_de: str | None = Field(None, description="Surface")
    techdaten: str | None = Field(None, description="Engineering Data")
    cssaas_mirrored_from: str | None = Field(None, description="Mirror Part ID")
    t_ersatz_fuer: str | None = Field(None, description="Replacement for")
    t_ersatz_durch: str | None = Field(None, description="Replaced by")
    din: str | None = Field(None, description="Norms")
    bemerkung: str | None = Field(None, description="Remarks")
    cdb_copy_of_item_id: str | None = Field(None, description="Copy of ID")
    type_object_id: str | None = Field(None, description="BOM Type ID")
    cdb_depends_on: str | None = Field(None, description="Derived from")
    site_object_id: str | None = Field(None, description="Plant")
    cssaas_frame_add_attr_1: str | None = Field(None, description="Additional Attribute 1")
    cssaas_frame_add_attr_2: str | None = Field(None, description="Additional Attribute 2")
    cssaas_frame_add_attr_3: str | None = Field(None, description="Additional Attribute 3")
    cssaas_frame_add_attr_4: str | None = Field(None, description="Additional Attribute 4")
    cssaas_frame_add_attr_5: str | None = Field(None, description="Additional Attribute 5")
    cdb_cpersno: str | None = Field(None, description="Created by")
    cdb_cpersno_name: str | None = Field(None, description="Created by")
    cdb_cdate: datetime | None = Field(None, description="Created on")
    cdb_mpersno: str | None = Field(None, description="Last Modified by")
    cdb_mpersno_name: str | None = Field(None, description="Last Modified by")
    cdb_mdate: datetime | None = Field(None, description="Last Modified on")
    cdb_m2persno: str | None = Field(None, description="File Last Saved by")
    cdb_m2persno_name: str | None = Field(None, description="File Last Saved by")
    cdb_m2date: datetime | None = Field(None, description="File Last Saved on")
    st_durchmesser: float | None = Field(None, description="Diameter")
    st_laenge: float | None = Field(None, description="Length")
    st_hoehe: float | None = Field(None, description="Height")
    cdb_object_id: str | None = Field(None, description="Object ID")
    site_erp: str | None = Field(None, description="Plant")
    fertart: str | None = Field(None, description="Production Type")
    t_pruef_datum: datetime | None = Field(None, description="Release Date")
    oberflaeche: str | None = Field(None, description="Surface")
    mengeneinheit: str | None = Field(None, description="Unit of Measure")
    gebrauchsstand: str | None = Field(None, description="Usability")
    st_breite: float | None = Field(None, description="Width")

    document_ids: list[str] = Field([], description="List of document IDs, that were changed. (z_nummer@z_index)")
    documents: list["Document"] = Field([], exclude=True)

    def link_objects(self, data: "EventData"):
        from .document import Document

        if self.document_ids:
            documents = get_items_of_type(data, Document)
            self._link_documents(documents)

    def _link_documents(self, documents: list["Document"]):
        for document in documents:
            if f"{document.z_nummer}@{document.z_index}" in self.document_ids and document not in self.documents:
                self.documents.append(document)


class Material(BaseObject):
    object_type: Literal[ObjectType.MATERIAL] = ObjectType.MATERIAL

    cdb_object_id: str | None = Field(None, description="Object ID")
    material_index: str | None = Field(None, description="Material Index")
    material_id: str | None = Field(None, description="Material ID")
    name_de: str | None = Field(None, description="Name DE")
    name_en: str | None = Field(None, description="Name EN")
    short_name: str | None = Field(None, description="Short Name")
    application: str | None = Field(None, description="Applications")
    remark: str | None = Field(None, description="Remarks")


class BOMItem(BaseObject):
    object_type: Literal[ObjectType.BOM_ITEM] = ObjectType.BOM_ITEM

    baugruppe: str | None = Field(None, description="Assembly")
    b_index: str | None = Field(None, description="Assembly Index")
    component_materialnr_erp: str | None = Field(None, description="Material Number ERP Component")
    netto_durchm: float | None = Field(None, description="Net. Diameter")
    netto_hoehe: float | None = Field(None, description="Net. Height")
    netto_laenge: float | None = Field(None, description="Net. Length")
    netto_breite: float | None = Field(None, description="Net. Width")
    position: int | None = Field(None, description="Position")
    menge: float | None = Field(None, description="Quantity")
    stlbemerkung: str | None = Field(None, description="Remarks")
    mengeneinheit: str | None = Field(None, description="Unit of Measure")
    teilenummer: str = Field(..., description="part number")
    t_index: str = Field(..., description="part index")

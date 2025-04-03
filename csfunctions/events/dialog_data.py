from typing import Literal

from pydantic import BaseModel, Field


class DocumentReleasedDialogData(BaseModel):
    dialog_type: Literal["document_release"] = "document_release"
    cdbprot_remark: str | None = Field(None, description="remark")
    cdb_ec_id: str | None = Field(None, description="Engineering Change ID")


class PartReleasedDialogData(BaseModel):
    dialog_type: Literal["part_release"] = "part_release"
    cdbprot_remark: str | None = Field("", description="remark")
    cdb_ec_id: str | None = Field("", description="Engineering Change ID")

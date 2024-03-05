from datetime import datetime
from typing import Literal

from pydantic import Field

from .base import BaseObject, ObjectType


class File(BaseObject):
    object_type: Literal[ObjectType.FILE] = ObjectType.FILE

    cdb_object_id: str = Field(..., description="ID")

    cdbf_name: str | None = Field(..., description="file name")
    cdbf_type: str | None = Field(..., description="file type")

    cdb_cpersno: str | None = Field("", description="Created by")
    mapped_cdb_cpersno_name: str | None = Field("", description="Created by")
    cdb_cdate: datetime | None = Field(None, description="Created on")

    cdb_mpersno: str | None = Field("", description="Last Modified by")
    mapped_cdb_mpersno_name: str | None = Field("", description="Last Modified by")
    cdb_mdate: datetime | None = Field(None, description="Last Modified on")

    blob_url: str | None = Field(None, description="Presigned Blob URL")

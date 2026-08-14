from typing import Literal

from pydantic import Field

from csfunctions.objects.base import BaseObject, ObjectType


class CommonRole(BaseObject):
    """
    A Common (global) Role that can be assigned to a Person.
    """

    object_type: Literal[ObjectType.COMMON_ROLE] = ObjectType.COMMON_ROLE

    role_id: str = Field(..., description="Role ID")
    name_de: str | None = Field(None, description="Name DE")
    name_en: str | None = Field(None, description="Name EN")
    name_ja: str | None = Field(None, description="Name JA")
    name_zh: str | None = Field(None, description="Name ZH")
    cdb_object_id: str | None = Field(None, description="Object ID")

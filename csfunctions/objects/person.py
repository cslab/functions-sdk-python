from typing import Literal

from pydantic import Field

from csfunctions.objects.base import BaseObject, ObjectType


class Person(BaseObject):
    object_type: Literal[ObjectType.PERSON] = ObjectType.PERSON

    personalnummer: str = Field(..., description="Personal Number")
    name: str = Field(..., description="System-Name")
    firstname: str | None = Field(None, description="First Name")
    lastname: str | None = Field(None, description="Last Name")
    gender: str | None = Field(None, description="Gender")
    title: str | None = Field(None, description="Title")
    initials: str | None = Field(None, description="Initials")
    active_account: bool | None = Field(None, description="Active Account")
    org_id: str | None = Field(None, description="Organization ID")
    abt_nummer: str | None = Field(None, description="Department Number")
    e_mail: str | None = Field(None, description="Email")
    telefon: str | None = Field(None, description="Phone")

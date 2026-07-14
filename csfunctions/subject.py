from typing import Literal

from pydantic import BaseModel, Field


class Subject(BaseModel):
    subject_id: str = Field(..., description="ID of the subject, eg. a role name or personalnummer")
    subject_type: Literal["Person", "PCS Role", "Common Role"] = Field(
        ..., description="Type of the subject: Person, PCS Role or Common Role"
    )

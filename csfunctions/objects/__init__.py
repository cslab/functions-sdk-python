from typing import Annotated

from pydantic import Field

from .base import BaseObject
from .briefcase import Briefcase
from .classification import ObjectPropertyValue
from .document import CADDocument, Document
from .engineering_change import Change, ChangeOrder, ChangeRequest, EngineeringChange
from .file import File
from .part import BOMItem, Material, MaturityLevel, Part
from .person import Person
from .workflow import Workflow

Object = Annotated[
    Document
    | CADDocument
    | Part
    | File
    | EngineeringChange
    | ChangeOrder
    | ChangeRequest
    | Material
    | BOMItem
    | ObjectPropertyValue
    | Briefcase
    | Workflow
    | Person
    | MaturityLevel,
    Field(discriminator="object_type"),
]


__all__ = [
    "Document",
    "CADDocument",
    "Part",
    "File",
    "EngineeringChange",
    "Change",
    "ChangeOrder",
    "ChangeRequest",
    "Material",
    "BOMItem",
    "ObjectPropertyValue",
    "Briefcase",
    "Workflow",
    "BaseObject",
    "Person",
    "MaturityLevel",
]
